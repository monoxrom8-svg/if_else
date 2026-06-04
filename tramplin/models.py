import json
import re
import requests

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


def _geocode_ru_postal_zippopotam(postal_code):
    """Запасной источник координат по РФ-индексу (Nominatim покрывает не все индексы)."""
    try:
        resp = requests.get(
            f"https://api.zippopotam.us/ru/{postal_code}",
            timeout=6,
        )
        if resp.status_code != 200:
            return None, None
        data = resp.json()
        places = data.get("places") or []
        if not places:
            return None, None
        place = places[0]
        return float(place["latitude"]), float(place["longitude"])
    except Exception:
        return None, None


def _geocode_open_meteo(name):
    """Города и населённые пункты РФ (работает, когда Nominatim недоступен)."""
    if not name or len(name.strip()) < 2:
        return None, None
    try:
        resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": name.strip(),
                "count": 1,
                "language": "ru",
                "country_code": "RU",
            },
            timeout=10,
        )
        if resp.status_code != 200:
            return None, None
        results = resp.json().get("results") or []
        if not results:
            return None, None
        row = results[0]
        return float(row["latitude"]), float(row["longitude"])
    except Exception:
        return None, None


def _nominatim_search(**params):
    """Запрос к Nominatim с корректным User-Agent (с браузера часто 403)."""
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"format": "json", "limit": 1, "accept-language": "ru", **params},
            headers={"User-Agent": "tramplin-app/1.0 (contact: tramplin@local)"},
            timeout=5,
        )
        if resp.status_code != 200:
            return None, None
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None, None


def geocode_detailed(address):
    """
    Геокодирование адреса/индекса.
    Возвращает (lat, lng, precision) или (None, None, None).
    precision: postal | street | city
    """
    if not address:
        return None, None, None
    address = address.strip()
    low = address.lower()
    if low in ("онлайн", "удалённо", "remote", "online", "—", "-"):
        return None, None, None

    def _nominatim_q(q, precision="street"):
        lat, lng = _nominatim_search(q=q)
        return (lat, lng, precision) if lat is not None else None

    def _open_meteo_q(name):
        lat, lng = _geocode_open_meteo(name)
        return (lat, lng, "city") if lat is not None else None

    # Только российский индекс (6 цифр)
    if re.fullmatch(r"\d{6}", address):
        lat, lng = _nominatim_search(postalcode=address, countrycodes="ru")
        if lat is not None:
            return lat, lng, "postal"
        for q in (f"{address}, Россия", f"{address}, Russia"):
            hit = _nominatim_q(q, "postal")
            if hit:
                return hit
        lat, lng = _geocode_ru_postal_zippopotam(address)
        if lat is not None:
            return lat, lng, "postal"
        return None, None, None

    parts = [p.strip() for p in address.split(",") if p.strip()]

    nominatim_queries = [address]
    if "россия" not in low and "russia" not in low:
        nominatim_queries.append(f"{address}, Россия")

    for q in nominatim_queries:
        hit = _nominatim_q(q, "street")
        if hit:
            return hit

    # Open-Meteo: город обычно первая часть до запятой
    city_candidates = []
    if parts:
        city_candidates.append(parts[0])
    if len(parts) > 1:
        city_candidates.extend(parts[1:])
    seen = set()
    for name in city_candidates:
        key = name.lower()
        if key in seen or len(name) < 2:
            continue
        seen.add(key)
        hit = _open_meteo_q(name)
        if hit:
            return hit

    return None, None, None


def geocode(address):
    """Геокодирование. Возвращает (lat, lng) или (None, None)."""
    lat, lng, _ = geocode_detailed(address)
    return lat, lng


class User(AbstractUser):
    ROLE_SEEKER = "seeker"
    ROLE_EMPLOYER = "employer"
    ROLE_CURATOR = "curator"
    ROLE_CHOICES = [
        (ROLE_SEEKER, "Соискатель"),
        (ROLE_EMPLOYER, "Работодатель"),
        (ROLE_CURATOR, "Куратор"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_SEEKER)
    is_blocked = models.BooleanField("Заблокирован", default=False)
    blocked_reason = models.CharField("Причина блокировки", max_length=300, blank=True)
    blocked_until = models.DateTimeField("Заблокирован до", null=True, blank=True)
    blocked_by_id_val = models.IntegerField("ID заблокировавшего", null=True, blank=True)
    blocked_by_name = models.CharField("Имя заблокировавшего", max_length=150, blank=True)
    display_name = models.CharField("Отображаемое имя", max_length=150, blank=True)

    # Employer verification fields
    inn = models.CharField("ИНН", max_length=12, blank=True)
    corporate_email = models.EmailField("Корпоративный email", blank=True)
    professional_network_url = models.URLField("Ссылка на профиль (LinkedIn/Habr)", blank=True)
    is_verified_employer = models.BooleanField("Верифицированный работодатель", default=False)

    # Employer profile
    company_name = models.CharField("Название компании", max_length=200, blank=True)
    company_description = models.TextField("Краткое описание", blank=True)
    company_industry = models.CharField("Отрасль", max_length=100, blank=True)
    company_website = models.URLField("Сайт компании", blank=True)
    company_video_url = models.URLField("Видео-презентация (YouTube/Vimeo)", blank=True)

    # Seeker profile
    university = models.CharField("Университет", max_length=200, blank=True)
    graduation_year = models.CharField("Год выпуска / Курс", max_length=20, blank=True)
    skills = models.TextField("Навыки (через запятую)", blank=True)
    github_url = models.URLField("GitHub / GitLab", blank=True)
    portfolio_url = models.URLField("Портфолио", blank=True)
    about = models.TextField("О себе", blank=True)

    def __str__(self):
        return self.display_name or self.username

    @property
    def skills_list(self):
        return [s.strip() for s in (self.skills or "").split(",") if s.strip()]

    @property
    def is_curator(self):
        return self.role == self.ROLE_CURATOR

    @property
    def is_superadmin(self):
        return self.is_superuser

    # Privacy settings
    is_profile_public = models.BooleanField("Публичный профиль (нетворкинг)", default=False)

    # Mentor flag — set automatically when a MentorApplication is approved
    is_mentor = models.BooleanField(
        "Верифицированный ментор",
        default=False,
        db_index=True,
        help_text="Устанавливается автоматически при одобрении заявки на менторство.",
    )

    # Mentor activity tracking
    MENTOR_STATUS_AVAILABLE = "available"
    MENTOR_STATUS_BUSY = "busy"
    MENTOR_STATUS_CHOICES = [
        (MENTOR_STATUS_AVAILABLE, "Доступен"),
        (MENTOR_STATUS_BUSY, "Занят"),
    ]
    mentor_status = models.CharField(
        "Статус ментора",
        max_length=20,
        choices=MENTOR_STATUS_CHOICES,
        default=MENTOR_STATUS_AVAILABLE,
        db_index=True,
        help_text="Автоматически переключается в «Занят» при 3 днях неактивности.",
    )
    last_message_sent_at = models.DateTimeField(
        "Последнее сообщение отправлено",
        null=True,
        blank=True,
        help_text="Обновляется автоматически при каждой отправке сообщения ментором.",
    )

    # Avatar
    avatar = models.FileField(
        "Фото профиля",
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    # Favorites: Opportunity.pk values (JSON array of integers)
    favorite_ids = models.TextField("Избранные вакансии (JSON)", default="[]", blank=True)

    @property
    def avatar_url(self):
        """Returns avatar URL or empty string (templates use |default filter)."""
        if self.avatar:
            return self.avatar.url
        return ""

    @property
    def mentorship_status(self):
        """Return the current MentorApplication status for this user.

        Returns MentorApplication.STATUS_NOT_APPLIED if no application exists.
        """
        try:
            return self.mentor_application.status
        except MentorApplication.DoesNotExist:
            return MentorApplication.STATUS_NOT_APPLIED


class Opportunity(models.Model):
    TYPE_VACANCY = "vacancy"
    TYPE_INTERNSHIP = "internship"
    TYPE_EVENT = "event"
    TYPE_MENTORSHIP = "mentorship"
    TYPE_CHOICES = [
        (TYPE_VACANCY, "Вакансия"),
        (TYPE_INTERNSHIP, "Стажировка"),
        (TYPE_EVENT, "Мероприятие"),
        (TYPE_MENTORSHIP, "Менторская программа"),
    ]

    FORMAT_REMOTE = "remote"
    FORMAT_HYBRID = "hybrid"
    FORMAT_OFFICE = "office"
    FORMAT_CHOICES = [
        (FORMAT_REMOTE, "Удалённо"),
        (FORMAT_HYBRID, "Гибрид"),
        (FORMAT_OFFICE, "Офис"),
    ]

    STATUS_ACTIVE = "active"
    STATUS_CLOSED = "closed"
    STATUS_PLANNED = "planned"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Активна"),
        (STATUS_CLOSED, "Закрыта"),
        (STATUS_PLANNED, "Запланирована"),
    ]

    MODERATION_PENDING = "pending"
    MODERATION_APPROVED = "approved"
    MODERATION_REJECTED = "rejected"
    MODERATION_CHOICES = [
        (MODERATION_PENDING, "На модерации"),
        (MODERATION_APPROVED, "Одобрено"),
        (MODERATION_REJECTED, "Отклонено"),
    ]

    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opportunities")
    company_display = models.CharField(
        "Компания (отображение)", max_length=200, blank=True, default=""
    )
    title = models.CharField("Название", max_length=200)
    type = models.CharField("Тип", max_length=20, choices=TYPE_CHOICES, default=TYPE_VACANCY)
    format = models.CharField("Формат", max_length=20, choices=FORMAT_CHOICES, default=FORMAT_REMOTE)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    moderation_status = models.CharField(
        "Статус модерации", max_length=20,
        choices=MODERATION_CHOICES, default=MODERATION_PENDING
    )
    salary = models.CharField("Зарплата / Вознаграждение", max_length=100, blank=True)
    location = models.CharField("Город / Адрес", max_length=200, blank=True)
    postal_code = models.CharField("Почтовый индекс", max_length=12, blank=True)
    latitude = models.FloatField("Широта", null=True, blank=True)
    longitude = models.FloatField("Долгота", null=True, blank=True)
    description = models.TextField("Описание")
    requirements = models.TextField("Требования", blank=True)
    skills_required = models.TextField("Необходимые навыки (через запятую)", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField("Дата окончания", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.employer.company_name or self.employer.display_name}"

    @property
    def skills_list(self):
        return [s.strip() for s in (self.skills_required or "").split(",") if s.strip()]

    @property
    def type_label(self):
        labels = {
            "vacancy": "Вакансия",
            "internship": "Стажировка",
            "event": "Мероприятие",
            "mentorship": "Менторская программа",
        }
        return labels.get(self.type, self.type)

    @property
    def format_label(self):
        labels = {"remote": "Удалённо", "hybrid": "Гибрид", "office": "Офис"}
        return labels.get(self.format, self.format)


class OpportunitySubmission(models.Model):
    """Предложение возможности от соискателя — публикуется после одобрения админом."""

    MODERATION_PENDING = "pending"
    MODERATION_APPROVED = "approved"
    MODERATION_REJECTED = "rejected"
    MODERATION_CHOICES = [
        (MODERATION_PENDING, "На модерации"),
        (MODERATION_APPROVED, "Одобрено"),
        (MODERATION_REJECTED, "Отклонено"),
    ]

    submitter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="opportunity_submissions"
    )
    company_name = models.CharField("Компания / организатор", max_length=200)
    title = models.CharField("Название", max_length=200)
    type = models.CharField(
        "Тип", max_length=20, choices=Opportunity.TYPE_CHOICES, default=Opportunity.TYPE_INTERNSHIP
    )
    format = models.CharField(
        "Формат", max_length=20, choices=Opportunity.FORMAT_CHOICES, default=Opportunity.FORMAT_OFFICE
    )
    salary = models.CharField("Зарплата / вознаграждение", max_length=100, blank=True)
    location = models.CharField("Адрес", max_length=300, blank=True)
    postal_code = models.CharField("Почтовый индекс", max_length=12, blank=True)
    latitude = models.FloatField("Широта", null=True, blank=True)
    longitude = models.FloatField("Долгота", null=True, blank=True)
    description = models.TextField("Описание")
    requirements = models.TextField("Требования", blank=True)
    skills_required = models.TextField("Навыки", blank=True)
    expires_at = models.DateField("Дата окончания", null=True, blank=True)
    moderation_status = models.CharField(
        max_length=20, choices=MODERATION_CHOICES, default=MODERATION_PENDING
    )
    admin_comment = models.CharField("Комментарий модератора", max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    published_opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="source_submission",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.submitter}"

    @property
    def type_label(self):
        return dict(Opportunity.TYPE_CHOICES).get(self.type, self.type)

    @property
    def format_label(self):
        return dict(Opportunity.FORMAT_CHOICES).get(self.format, self.format)


class Application(models.Model):
    STATUS_NEW = "new"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    STATUS_RESERVE = "reserve"
    STATUS_CHOICES = [
        (STATUS_NEW, "Новая"),
        (STATUS_ACCEPTED, "Принят"),
        (STATUS_REJECTED, "Отклонён"),
        (STATUS_RESERVE, "В резерве"),
    ]

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    cover_letter = models.TextField("Сопроводительное письмо", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("opportunity", "applicant")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.applicant} → {self.opportunity}"


class Contact(models.Model):
    """Contact request between two seekers. pending → accepted lifecycle."""
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Ожидает подтверждения"),
        (STATUS_ACCEPTED, "Принят"),
    ]

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contacts_sent"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contacts_received"
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_user} → {self.to_user} [{self.status}]"


class CompanyProfile(models.Model):
    """Extended culture & tech stack data for an employer's company page."""
    employer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="company_profile"
    )
    # Cover / office photo URL (external link or relative path)
    cover_image_url = models.URLField("Обложка (URL фото офиса)", blank=True)
    # Tech stack stored as JSON: {"Backend": ["Go","Python"], "Frontend": ["React","Next.js"], ...}
    tech_stack_json = models.TextField("Технологии (JSON)", default="{}", blank=True)
    # Core values stored as JSON list: [{"emoji":"🚀","title":"...","desc":"..."}]
    values_json = models.TextField("Ценности (JSON)", default="[]", blank=True)
    # Perks stored as JSON list: [{"icon":"💻","title":"MacBook Pro"}]
    perks_json = models.TextField("Преимущества (JSON)", default="[]", blank=True)
    # Social links
    linkedin_url = models.URLField("LinkedIn компании", blank=True)
    telegram_url = models.URLField("Telegram-канал", blank=True)
    vk_url = models.URLField("ВКонтакте", blank=True)
    # Location text
    office_address = models.CharField("Адрес офиса", max_length=300, blank=True)
    office_latitude = models.FloatField("Широта офиса", null=True, blank=True)
    office_longitude = models.FloatField("Долгота офиса", null=True, blank=True)
    founded_year = models.CharField("Год основания", max_length=10, blank=True)
    team_size = models.CharField("Размер команды", max_length=50, blank=True)

    def __str__(self):
        return f"Профиль компании: {self.employer.company_name or self.employer.display_name}"

    @property
    def tech_stack(self):
        try:
            return json.loads(self.tech_stack_json or "{}")
        except (ValueError, TypeError):
            return {}

    @property
    def values(self):
        try:
            return json.loads(self.values_json or "[]")
        except (ValueError, TypeError):
            return []

    @property
    def perks(self):
        try:
            return json.loads(self.perks_json or "[]")
        except (ValueError, TypeError):
            return []


class CompanyReview(models.Model):
    """User review for a company."""
    company = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews",
        limit_choices_to={"role": "employer"}
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_written"
    )
    rating = models.PositiveSmallIntegerField("Оценка (1–5)", default=5)
    text = models.TextField("Текст отзыва")
    vacancy_tag = models.CharField("Вакансия (опционально)", max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField("Прошёл модерацию", default=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("company", "author")

    def __str__(self):
        return f"{self.author} → {self.company.company_name}: {self.rating}★"


class Message(models.Model):
    """Direct message between two users, with optional file attachment."""
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_sent"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_received"
    )
    text = models.TextField("Текст", blank=True)
    file_attachment = models.FileField(
        "Вложение", upload_to="chat_attachments/%Y/%m/", blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender} → {self.receiver} [{self.timestamp:%d.%m %H:%M}]"

    @property
    def file_name(self):
        if self.file_attachment:
            return self.file_attachment.name.split("/")[-1]
        return ""

    @property
    def is_image(self):
        if self.file_attachment:
            ext = self.file_name.rsplit(".", 1)[-1].lower()
            return ext in ("jpg", "jpeg", "png", "gif", "webp")
        return False


# ── Автогеокодинг ─────────────────────────────────────────────────────────────

def employer_company_display(employer):
    """Название компании для карточки объявления."""
    if not employer:
        return ""
    name = (employer.company_name or "").strip()
    if name:
        return name[:200]
    return (employer.display_name or employer.username or "")[:200]


@receiver(pre_save, sender=Opportunity)
def set_opportunity_company_display(sender, instance, **kwargs):
    if not (instance.company_display or "").strip():
        instance.company_display = employer_company_display(instance.employer)


@receiver(pre_save, sender=Opportunity)
def reset_opportunity_coords_on_location_change(sender, instance, **kwargs):
    """Сбрасывает координаты если адрес или индекс изменились."""
    if instance.pk:
        try:
            old = Opportunity.objects.get(pk=instance.pk)
            if old.location != instance.location or old.postal_code != instance.postal_code:
                instance.latitude = None
                instance.longitude = None
        except Opportunity.DoesNotExist:
            pass


@receiver(post_save, sender=Opportunity)
def geocode_opportunity(sender, instance, **kwargs):
    """Геокодирует адрес или индекс при сохранении, если координаты ещё не заданы."""
    if instance.latitude is not None and instance.longitude is not None:
        return
    queries = []
    if instance.location:
        queries.append(instance.location)
    if instance.postal_code:
        queries.append(f"{instance.postal_code}, Россия")
        if instance.location:
            queries.append(f"{instance.postal_code}, {instance.location}, Россия")
    for q in queries:
        lat, lng = geocode(q)
        if lat is not None:
            Opportunity.objects.filter(pk=instance.pk).update(latitude=lat, longitude=lng)
            break


@receiver(pre_save, sender=CompanyProfile)
def reset_company_coords_on_address_change(sender, instance, **kwargs):
    """Сбрасывает координаты если адрес офиса изменился."""
    if instance.pk:
        try:
            old = CompanyProfile.objects.get(pk=instance.pk)
            if old.office_address != instance.office_address:
                instance.office_latitude = None
                instance.office_longitude = None
        except CompanyProfile.DoesNotExist:
            pass


@receiver(post_save, sender=CompanyProfile)
def geocode_company_profile(sender, instance, **kwargs):
    """Геокодирует office_address при сохранении, если координаты ещё не заданы."""
    if instance.office_address and (instance.office_latitude is None or instance.office_longitude is None):
        lat, lng = geocode(instance.office_address)
        if lat is not None:
            CompanyProfile.objects.filter(pk=instance.pk).update(
                office_latitude=lat, office_longitude=lng
            )


# ── Активность ментора ────────────────────────────────────────────────────────

@receiver(post_save, sender=Message)
def update_mentor_last_message(sender, instance, created, **kwargs):
    """При каждом новом сообщении от ментора обновляет last_message_sent_at
    и сбрасывает статус обратно в «Доступен», если он был «Занят»."""
    if not created:
        return
    sender_user = instance.sender
    if not sender_user.is_mentor:
        return
    # Используем update() чтобы не триггерить лишние сигналы
    User.objects.filter(pk=sender_user.pk).update(
        last_message_sent_at=instance.timestamp,
        mentor_status=User.MENTOR_STATUS_AVAILABLE,
    )


class Recommendation(models.Model):
    """Opportunity recommendation sent from one user to a contact."""
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recommendations_sent"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recommendations_received"
    )
    opportunity_id = models.IntegerField("ID вакансии")
    opportunity_title = models.CharField("Название вакансии", max_length=200)
    opportunity_company = models.CharField("Компания", max_length=200)
    message = models.TextField("Сообщение", blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.opportunity_title}"


class CuratorProfile(models.Model):
    """Расширенный профиль куратора — привязан к пользователю с ролью 'curator'."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="curator_profile",
        verbose_name="Пользователь",
    )
    # Зона ответственности, например: "Web-разработка, гр. 422ISV-2"
    responsibility_area = models.CharField(
        "Зона ответственности",
        max_length=300,
        blank=True,
        help_text='Например: "Web-разработка, гр. 422ISV-2"',
    )
    # График доступности, например: "Будни, 10:00 - 18:00"
    availability_schedule = models.CharField(
        "График доступности",
        max_length=200,
        blank=True,
        help_text='Например: "Будни, 10:00 - 18:00"',
    )
    # Количество одобренных менторов — обновляется при модерации заявок
    approved_mentors_count = models.IntegerField(
        "Количество одобренных менторов",
        default=0,
    )

    class Meta:
        verbose_name = "Профиль куратора"
        verbose_name_plural = "Профили кураторов"

    def __str__(self):
        return f"Куратор: {self.user.display_name or self.user.username}"


class ModerationLog(models.Model):
    """Журнал действий куратора при модерации контента."""

    ACTION_APPROVE_MENTOR = "approve_mentor"
    ACTION_REJECT_MENTOR = "reject_mentor"
    ACTION_APPROVE_OPP = "approve_opportunity"
    ACTION_REJECT_OPP = "reject_opportunity"
    ACTION_DELETE_OPP = "delete_opportunity"
    ACTION_BLOCK_USER = "block_user"
    ACTION_UNBLOCK_USER = "unblock_user"
    ACTION_MODERATE_REVIEW = "moderate_review"

    ACTION_CHOICES = [
        (ACTION_APPROVE_MENTOR, "Одобрил заявку на менторство"),
        (ACTION_REJECT_MENTOR, "Отклонил заявку на менторство"),
        (ACTION_APPROVE_OPP, "Одобрил объявление"),
        (ACTION_REJECT_OPP, "Отклонил объявление"),
        (ACTION_DELETE_OPP, "Удалил объявление"),
        (ACTION_BLOCK_USER, "Заблокировал пользователя"),
        (ACTION_UNBLOCK_USER, "Разблокировал пользователя"),
        (ACTION_MODERATE_REVIEW, "Модерировал отзыв"),
    ]

    curator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="moderation_logs",
        verbose_name="Куратор",
        limit_choices_to={"role": User.ROLE_CURATOR},
    )
    action = models.CharField(
        "Действие",
        max_length=50,
        choices=ACTION_CHOICES,
    )
    # Текстовое описание объекта, над которым выполнено действие
    target_description = models.CharField(
        "Описание объекта",
        max_length=300,
        blank=True,
    )
    created_at = models.DateTimeField("Дата и время", auto_now_add=True)

    class Meta:
        verbose_name = "Запись журнала модерации"
        verbose_name_plural = "Журнал модерации"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.curator} — {self.get_action_display()} [{self.created_at:%d.%m.%Y %H:%M}]"


class MentorApplication(models.Model):
    """Application submitted by a seeker who wishes to become a mentor.

    One-to-one with User: each user may have at most one mentor application.
    """

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_NOT_APPLIED = "not_applied"

    STATUS_CHOICES = [
        (STATUS_PENDING, "На рассмотрении"),
        (STATUS_APPROVED, "Одобрено"),
        (STATUS_REJECTED, "Отклонено"),
        (STATUS_NOT_APPLIED, "Не подавал заявку"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="mentor_application",
        verbose_name="Пользователь",
    )
    status = models.CharField(
        "Статус заявки",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
    )
    experience_description = models.TextField(
        "Описание опыта",
        help_text="Расскажите о своём профессиональном опыте и достижениях.",
    )
    skills_to_teach = models.TextField(
        "Навыки для передачи",
        help_text="Перечислите навыки и технологии, которым вы готовы обучать.",
    )
    applied_at = models.DateTimeField("Дата подачи заявки", auto_now_add=True)

    # Privacy consent — must be explicitly accepted before submission
    accepted_privacy_policy = models.BooleanField(
        "Политика конфиденциальности ментора принята",
        default=False,
        help_text="Пользователь принял Политику конфиденциальности программы менторства.",
    )
    accepted_terms_of_service = models.BooleanField(
        "Условия использования приняты",
        default=False,
        help_text="Пользователь принял Условия использования программы менторства.",
    )

    class Meta:
        verbose_name = "Заявка на менторство"
        verbose_name_plural = "Заявки на менторство"
        ordering = ["-applied_at"]

    def __str__(self):
        return f"Заявка на менторство: {self.user} [{self.get_status_display()}]"

    @property
    def is_approved(self):
        """Convenience check used in templates and business logic."""
        return self.status == self.STATUS_APPROVED

    @property
    def is_pending(self):
        return self.status == self.STATUS_PENDING
