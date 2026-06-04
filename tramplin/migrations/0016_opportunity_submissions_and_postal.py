from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tramplin", "0015_add_block_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="opportunity",
            name="postal_code",
            field=models.CharField(blank=True, max_length=12, verbose_name="Почтовый индекс"),
        ),
        migrations.CreateModel(
            name="OpportunitySubmission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company_name", models.CharField(max_length=200, verbose_name="Компания / организатор")),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("type", models.CharField(
                    choices=[
                        ("vacancy", "Вакансия"),
                        ("internship", "Стажировка"),
                        ("event", "Мероприятие"),
                        ("mentorship", "Менторская программа"),
                    ],
                    default="internship",
                    max_length=20,
                    verbose_name="Тип",
                )),
                ("format", models.CharField(
                    choices=[
                        ("remote", "Удалённо"),
                        ("hybrid", "Гибрид"),
                        ("office", "Офис"),
                    ],
                    default="office",
                    max_length=20,
                    verbose_name="Формат",
                )),
                ("salary", models.CharField(blank=True, max_length=100, verbose_name="Зарплата / вознаграждение")),
                ("location", models.CharField(blank=True, max_length=300, verbose_name="Адрес")),
                ("postal_code", models.CharField(blank=True, max_length=12, verbose_name="Почтовый индекс")),
                ("latitude", models.FloatField(blank=True, null=True, verbose_name="Широта")),
                ("longitude", models.FloatField(blank=True, null=True, verbose_name="Долгота")),
                ("description", models.TextField(verbose_name="Описание")),
                ("requirements", models.TextField(blank=True, verbose_name="Требования")),
                ("skills_required", models.TextField(blank=True, verbose_name="Навыки")),
                ("expires_at", models.DateField(blank=True, null=True, verbose_name="Дата окончания")),
                ("moderation_status", models.CharField(
                    choices=[
                        ("pending", "На модерации"),
                        ("approved", "Одобрено"),
                        ("rejected", "Отклонено"),
                    ],
                    default="pending",
                    max_length=20,
                )),
                ("admin_comment", models.CharField(blank=True, max_length=300, verbose_name="Комментарий модератора")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("published_opportunity", models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name="source_submission",
                    to="tramplin.opportunity",
                )),
                ("submitter", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="opportunity_submissions",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
