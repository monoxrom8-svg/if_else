from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from .models import (
    User, Opportunity, OpportunitySubmission, Application, Contact,
    Recommendation, CompanyProfile, CompanyReview, MentorApplication,
)


class InternshipProxy(Opportunity):
    """Proxy model so internships get their own admin section."""
    class Meta:
        proxy = True
        verbose_name = "Стажировка"
        verbose_name_plural = "Стажировки (модерация)"


class VacancyProxy(Opportunity):
    """Proxy model so vacancies get their own admin section."""
    class Meta:
        proxy = True
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии (модерация)"


class EventProxy(Opportunity):
    """Proxy model so events get their own admin section."""
    class Meta:
        proxy = True
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия (модерация)"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "display_name", "role", "is_verified_employer", "date_joined")
    list_filter = ("role", "is_verified_employer", "is_staff")
    search_fields = ("username", "email", "display_name", "company_name")
    readonly_fields = ("last_message_sent_at",)
    fieldsets = UserAdmin.fieldsets + (
        ("Роль и профиль", {
            "fields": (
                "role", "display_name", "about",
                "is_profile_public",
            )
        }),
        ("Профиль работодателя", {
            "fields": (
                "company_name", "company_description", "company_industry",
                "company_website", "company_video_url",
                "inn", "corporate_email", "professional_network_url",
                "is_verified_employer",
            )
        }),
        ("Профиль соискателя", {
            "fields": (
                "university", "graduation_year", "skills",
                "github_url", "portfolio_url",
            )
        }),
        ("Менторство", {
            "fields": ("is_mentor", "mentor_status", "last_message_sent_at"),
            "description": "Только суперпользователь или куратор может изменить эти поля вручную.",
        }),
    )


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "type", "format", "status", "moderation_status", "created_at", "expires_at")
    list_filter = ("type", "format", "status", "moderation_status")
    search_fields = ("title", "employer__company_name", "location")
    list_editable = ("status", "moderation_status")
    actions = ["approve_opportunities", "reject_opportunities"]

    @admin.action(description="✅ Одобрить выбранные")
    def approve_opportunities(self, request, queryset):
        updated = queryset.update(moderation_status=Opportunity.MODERATION_APPROVED)
        self.message_user(request, f"Одобрено: {updated} записей.")

    @admin.action(description="❌ Отклонить выбранные")
    def reject_opportunities(self, request, queryset):
        updated = queryset.update(moderation_status=Opportunity.MODERATION_REJECTED)
        self.message_user(request, f"Отклонено: {updated} записей.")


@admin.register(InternshipProxy)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "format", "status", "moderation_status", "created_at", "expires_at")
    list_filter = ("format", "status", "moderation_status")
    search_fields = ("title", "employer__company_name", "employer__display_name", "location", "skills_required")
    list_editable = ("moderation_status",)
    ordering = ("-created_at",)
    actions = ["approve_internships", "reject_internships"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=Opportunity.TYPE_INTERNSHIP)

    @admin.action(description="✅ Одобрить выбранные стажировки")
    def approve_internships(self, request, queryset):
        updated = queryset.update(moderation_status=Opportunity.MODERATION_APPROVED)
        self.message_user(request, f"Одобрено стажировок: {updated}.")

    @admin.action(description="❌ Отклонить выбранные стажировки")
    def reject_internships(self, request, queryset):
        updated = queryset.update(moderation_status=Opportunity.MODERATION_REJECTED)
        self.message_user(request, f"Отклонено стажировок: {updated}.")


@admin.register(VacancyProxy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "format", "salary", "status", "moderation_status", "created_at", "expires_at")
    list_filter = ("format", "status", "moderation_status")
    search_fields = ("title", "employer__company_name", "employer__display_name", "location", "skills_required")
    list_editable = ("moderation_status",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Основное", {"fields": ("employer", "title", "type", "format", "status", "moderation_status")}),
        ("Детали", {"fields": ("salary", "location", "description", "requirements", "skills_required", "expires_at")}),
        ("Служебное", {"fields": ("created_at",)}),
    )
    actions = ["approve_vacancies", "reject_vacancies"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=Opportunity.TYPE_VACANCY)

    @admin.action(description="✅ Одобрить выбранные вакансии")
    def approve_vacancies(self, request, queryset):
        updated = queryset.update(moderation_status=Opportunity.MODERATION_APPROVED)
        self.message_user(request, f"Одобрено вакансий: {updated}.")

    @admin.action(description="❌ Отклонить выбранные вакансии")
    def reject_vacancies(self, request, queryset):
        updated = queryset.update(moderation_status=Opportunity.MODERATION_REJECTED)
        self.message_user(request, f"Отклонено вакансий: {updated}.")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant", "opportunity", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("applicant__display_name", "opportunity__title")
    list_editable = ("status",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "created_at")
    search_fields = ("from_user__display_name", "to_user__display_name")


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "opportunity_title", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("sender__display_name", "recipient__display_name", "opportunity_title")


@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "company", "rating", "is_moderated", "created_at")
    list_filter = ("is_moderated", "rating")
    search_fields = ("author__display_name", "company__company_name", "text")
    list_editable = ("is_moderated",)


@admin.register(EventProxy)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "format", "status", "moderation_status", "expires_at", "created_at", "is_upcoming")
    list_filter = ("format", "status", "moderation_status")
    search_fields = ("title", "employer__company_name", "employer__display_name", "location", "description")
    list_editable = ("moderation_status",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Основное", {"fields": ("employer", "title", "type", "format", "status", "moderation_status")}),
        ("Детали мероприятия", {"fields": ("location", "description", "requirements", "skills_required", "salary", "expires_at")}),
        ("Служебное", {"fields": ("created_at",)}),
    )
    actions = ["approve_events", "archive_events", "reject_events"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=Opportunity.TYPE_EVENT)

    @admin.display(description="Предстоящее?", boolean=True)
    def is_upcoming(self, obj):
        if obj.expires_at:
            return obj.expires_at >= timezone.now().date()
        return True

    @admin.action(description="✅ Одобрить выбранные мероприятия")
    def approve_events(self, request, queryset):
        updated = queryset.update(moderation_status=Opportunity.MODERATION_APPROVED)
        self.message_user(request, f"Одобрено мероприятий: {updated}.")

    @admin.action(description="📦 Архивировать выбранные мероприятия")
    def archive_events(self, request, queryset):
        updated = queryset.update(status=Opportunity.STATUS_CLOSED)
        self.message_user(request, f"Архивировано мероприятий: {updated}.")

    @admin.action(description="❌ Отклонить выбранные мероприятия")
    def reject_events(self, request, queryset):
        updated = queryset.update(moderation_status=Opportunity.MODERATION_REJECTED)
        self.message_user(request, f"Отклонено мероприятий: {updated}.")


@admin.register(MentorApplication)
class MentorApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface for MentorApplication moderation.

    Default view shows only pending applications so curators land directly
    on the work queue. Approve/Reject actions atomically update both the
    application status and the user's is_mentor flag.
    """

    # ── List view ────────────────────────────────────────────────────────────
    list_display = (
        "applicant_name",
        "applicant_email",
        "skills_preview",
        "status_badge",
        "consents_ok",
        "applied_at",
    )
    list_filter = ("status",)
    search_fields = ("user__username", "user__display_name", "user__email", "skills_to_teach")
    readonly_fields = ("applied_at", "applicant_link")
    ordering = ("-applied_at",)
    date_hierarchy = "applied_at"
    actions = ["action_approve", "action_reject"]

    fieldsets = (
        ("Заявитель", {
            "fields": ("applicant_link", "status", "applied_at"),
        }),
        ("Содержание заявки", {
            "fields": ("experience_description", "skills_to_teach"),
        }),
        ("Правовые согласия", {
            "fields": ("accepted_privacy_policy", "accepted_terms_of_service"),
            "classes": ("collapse",),
        }),
    )

    # ── Default queryset: show pending first, then others ────────────────────
    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("user")
        # Annotate ordering: pending first
        from django.db.models import Case, IntegerField, When
        return qs.annotate(
            _order=Case(
                When(status=MentorApplication.STATUS_PENDING, then=0),
                When(status=MentorApplication.STATUS_APPROVED, then=1),
                When(status=MentorApplication.STATUS_REJECTED, then=2),
                default=3,
                output_field=IntegerField(),
            )
        ).order_by("_order", "-applied_at")

    # ── Custom display columns ───────────────────────────────────────────────
    @admin.display(description="Заявитель", ordering="user__display_name")
    def applicant_name(self, obj):
        from django.utils.html import format_html
        name = obj.user.display_name or obj.user.username
        return format_html('<strong>{}</strong>', name)

    @admin.display(description="Email", ordering="user__email")
    def applicant_email(self, obj):
        return obj.user.email

    @admin.display(description="Стек (превью)")
    def skills_preview(self, obj):
        from django.utils.html import format_html
        preview = obj.skills_to_teach[:60]
        if len(obj.skills_to_teach) > 60:
            preview += "…"
        return format_html('<span style="color:#475569;font-size:.8125rem;">{}</span>', preview)

    @admin.display(description="Статус")
    def status_badge(self, obj):
        from django.utils.html import format_html
        colours = {
            MentorApplication.STATUS_PENDING:  ("#FFFBEB", "#D97706", "На рассмотрении"),
            MentorApplication.STATUS_APPROVED: ("#EFF6FF", "#2563EB", "Одобрено ✓"),
            MentorApplication.STATUS_REJECTED: ("#F1F5F9", "#64748B", "Отклонено"),
        }
        bg, fg, label = colours.get(obj.status, ("#F1F5F9", "#64748B", obj.get_status_display()))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:20px;'
            'font-size:.75rem;font-weight:700;">{}</span>',
            bg, fg, label,
        )

    @admin.display(description="Согласия", boolean=True)
    def consents_ok(self, obj):
        return obj.accepted_privacy_policy and obj.accepted_terms_of_service

    @admin.display(description="Заявитель (ссылка)")
    def applicant_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse("admin:tramplin_user_change", args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.display_name or obj.user.username)

    # ── Bulk actions ─────────────────────────────────────────────────────────
    @admin.action(description="✅ Одобрить выбранные заявки")
    def action_approve(self, request, queryset):
        """Approve applications and grant is_mentor flag to each applicant."""
        approved_count = 0
        for app in queryset.select_related("user"):
            if app.status != MentorApplication.STATUS_APPROVED:
                app.status = MentorApplication.STATUS_APPROVED
                app.save(update_fields=["status"])
                # Grant mentor flag on the user profile
                User.objects.filter(pk=app.user.pk).update(is_mentor=True)
                approved_count += 1
        self.message_user(
            request,
            f"Одобрено заявок: {approved_count}. Статус «Верифицированный ментор» присвоен.",
            level="success",
        )

    @admin.action(description="❌ Отклонить выбранные заявки")
    def action_reject(self, request, queryset):
        """Reject applications and revoke is_mentor flag if previously granted."""
        rejected_count = 0
        for app in queryset.select_related("user"):
            if app.status != MentorApplication.STATUS_REJECTED:
                app.status = MentorApplication.STATUS_REJECTED
                app.save(update_fields=["status"])
                # Revoke mentor flag
                User.objects.filter(pk=app.user.pk).update(is_mentor=False)
                rejected_count += 1
        self.message_user(
            request,
            f"Отклонено заявок: {rejected_count}.",
            level="warning",
        )


@admin.register(OpportunitySubmission)
class OpportunitySubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "submitter", "type", "moderation_status", "created_at")
    list_filter = ("moderation_status", "type", "format")
    search_fields = ("title", "submitter__username", "company_name", "location")
    readonly_fields = ("published_opportunity", "reviewed_at", "created_at")
