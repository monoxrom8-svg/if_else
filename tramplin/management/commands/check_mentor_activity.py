"""
Команда управления: check_mentor_activity
==========================================
Находит всех верифицированных менторов со статусом «Доступен» (available),
у которых последнее сообщение было отправлено более 3 дней назад (или не
отправлялось вовсе), и переключает их статус в «Занят» (busy).

Использование:
    python manage.py check_mentor_activity
    python manage.py check_mentor_activity --days 7   # изменить порог
    python manage.py check_mentor_activity --dry-run  # только показать, не менять
"""

import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from tramplin.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Переключает статус менторов в «Занят», если они не отправляли "
        "сообщений дольше заданного порога (по умолчанию 3 дня)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=3,
            metavar="N",
            help="Порог неактивности в днях (по умолчанию: 3).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
            help="Показать, кто будет переключён, без реального изменения данных.",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]
        cutoff = timezone.now() - timezone.timedelta(days=days)

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f"\n{'[ТЕСТ] ' if dry_run else ''}Проверка активности менторов "
                f"(порог: {days} дн., граница: {cutoff:%d.%m.%Y %H:%M} UTC)\n"
            )
        )

        # Строим правильный Q-фильтр
        from django.db.models import Q
        inactive_qs = User.objects.filter(
            is_mentor=True,
            mentor_status=User.MENTOR_STATUS_AVAILABLE,
        ).filter(
            Q(last_message_sent_at__lt=cutoff) | Q(last_message_sent_at__isnull=True)
        )

        count = inactive_qs.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("  Неактивных менторов не найдено. Всё в порядке."))
            logger.info("check_mentor_activity: неактивных менторов не найдено (порог %d дн.)", days)
            return

        # Вывод списка затронутых менторов
        self.stdout.write(f"  Найдено менторов для переключения: {self.style.WARNING(str(count))}\n")
        for mentor in inactive_qs.order_by("display_name", "username"):
            last = mentor.last_message_sent_at
            last_str = last.strftime("%d.%m.%Y %H:%M") if last else "никогда"
            self.stdout.write(
                f"    • {mentor.display_name or mentor.username} "
                f"(id={mentor.pk}) — последнее сообщение: {last_str}"
            )

        if dry_run:
            self.stdout.write(
                self.style.WARNING("\n  [ТЕСТ] Изменения не применены (--dry-run).\n")
            )
            logger.info(
                "check_mentor_activity [dry-run]: %d менторов были бы переключены в «Занят».",
                count,
            )
            return

        # Применяем изменения одним UPDATE-запросом
        updated = inactive_qs.update(mentor_status=User.MENTOR_STATUS_BUSY)

        self.stdout.write(
            self.style.SUCCESS(
                f"\n  ✓ Переключено в «Занят»: {updated} ментор(ов).\n"
            )
        )
        logger.info(
            "check_mentor_activity: %d ментор(ов) переключено в статус «Занят» "
            "(порог неактивности: %d дн.).",
            updated,
            days,
        )
