from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import FileExtensionValidator
from .models import User, Opportunity, OpportunitySubmission, CompanyProfile, CompanyReview, CuratorProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
    )
    display_name = forms.CharField(
        label="Отображаемое имя",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Иван Иванов"}),
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.HiddenInput(),
        initial=User.ROLE_SEEKER,
    )
    inn = forms.CharField(
        label="ИНН компании", max_length=12, required=False,
        widget=forms.TextInput(attrs={"placeholder": "7700000000"}),
    )
    corporate_email = forms.EmailField(
        label="Корпоративный email", required=False,
        widget=forms.EmailInput(attrs={"placeholder": "hr@company.ru"}),
    )
    professional_network_url = forms.URLField(
        label="LinkedIn / Habr Career", required=False,
        widget=forms.URLInput(attrs={"placeholder": "https://linkedin.com/in/..."}),
    )

    class Meta:
        model = User
        fields = ("email", "display_name", "role", "password1", "password2",
                  "inn", "corporate_email", "professional_network_url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["placeholder"] = "Минимум 8 символов"
        self.fields["password2"].widget.attrs["placeholder"] = "Повторите пароль"
        if "username" in self.fields:
            self.fields["username"].required = False

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower().strip()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        if role == User.ROLE_EMPLOYER:
            if not cleaned.get("inn"):
                self.add_error("inn", "ИНН обязателен для работодателей.")
            if not cleaned.get("corporate_email"):
                self.add_error("corporate_email", "Корпоративный email обязателен.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower().strip()
        user.email = email
        user.username = email
        user.display_name = self.cleaned_data["display_name"]
        user.role = self.cleaned_data["role"]
        user.inn = self.cleaned_data.get("inn", "")
        user.corporate_email = self.cleaned_data.get("corporate_email", "")
        user.professional_network_url = self.cleaned_data.get("professional_network_url", "")
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Ваш пароль", "autocomplete": "current-password"}),
    )
    remember_me = forms.BooleanField(required=False, label="Запомнить меня")


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("display_name", "company_name", "company_description",
                  "company_industry", "company_website", "company_video_url",
                  "professional_network_url")
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "Как отображается в чате и кабинете"}),
            "company_name": forms.TextInput(attrs={"placeholder": "ООО Ромашка"}),
            "company_description": forms.Textarea(attrs={"rows": 3, "placeholder": "Краткое описание компании..."}),
            "company_industry": forms.TextInput(attrs={"placeholder": "Финтех, EdTech, DevTools..."}),
            "company_website": forms.URLInput(attrs={"placeholder": "https://company.ru"}),
            "company_video_url": forms.URLInput(attrs={"placeholder": "https://youtube.com/..."}),
            "professional_network_url": forms.URLInput(attrs={"placeholder": "https://linkedin.com/company/..."}),
        }
        labels = {
            "display_name": "Ваше имя",
            "company_name": "Название компании",
            "company_description": "Описание",
            "company_industry": "Отрасль",
            "company_website": "Сайт",
            "company_video_url": "Видео-презентация",
            "professional_network_url": "LinkedIn / Habr",
        }


class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("display_name", "university", "graduation_year",
                  "skills", "github_url", "portfolio_url", "about")
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "Иван Иванов"}),
            "university": forms.TextInput(attrs={"placeholder": "МГУ, МФТИ, НИУ ВШЭ..."}),
            "graduation_year": forms.TextInput(attrs={"placeholder": "2026 / 3 курс"}),
            "skills": forms.TextInput(attrs={"placeholder": "Python, React, SQL, Docker..."}),
            "github_url": forms.URLInput(attrs={"placeholder": "https://github.com/username"}),
            "portfolio_url": forms.URLInput(attrs={"placeholder": "https://myportfolio.ru"}),
            "about": forms.Textarea(attrs={"rows": 3, "placeholder": "Расскажите о себе..."}),
        }
        labels = {
            "display_name": "Полное имя",
            "university": "Университет",
            "graduation_year": "Год выпуска / Курс",
            "skills": "Навыки",
            "github_url": "GitHub / GitLab",
            "portfolio_url": "Портфолио",
            "about": "О себе",
        }


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ("title", "type", "format", "status", "salary",
                  "location", "postal_code", "description", "requirements", "skills_required", "expires_at")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Python Backend Developer"}),
            "salary": forms.TextInput(attrs={"placeholder": "150 000 — 200 000 ₽"}),
            "location": forms.TextInput(attrs={"placeholder": "Москва, Тверская улица, 7"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "123456"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Описание вакансии..."}),
            "requirements": forms.Textarea(attrs={"rows": 3, "placeholder": "Требования к кандидату..."}),
            "skills_required": forms.TextInput(attrs={"placeholder": "Python, Django, PostgreSQL"}),
            "expires_at": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": "Название",
            "type": "Тип",
            "format": "Формат",
            "status": "Статус",
            "salary": "Зарплата / Вознаграждение",
            "location": "Город / Адрес",
            "postal_code": "Почтовый индекс",
            "description": "Описание",
            "requirements": "Требования",
            "skills_required": "Навыки (через запятую)",
            "expires_at": "Дата окончания",
        }

    def clean(self):
        cleaned = super().clean()
        _validate_map_location(self.data, cleaned)
        return cleaned


def _validate_map_location(data, cleaned):
    """Требует подтверждённую точку на карте для офиса/гибрида."""
    fmt = cleaned.get("format")
    if fmt not in (Opportunity.FORMAT_OFFICE, Opportunity.FORMAT_HYBRID):
        return
    lat = data.get("latitude")
    lng = data.get("longitude")
    confirmed = data.get("location_confirmed") == "1"
    location = (cleaned.get("location") or "").strip()
    postal = (cleaned.get("postal_code") or "").strip()
    if not confirmed or not lat or not lng:
        if not location and not postal:
            raise forms.ValidationError(
                "Для офисного или гибридного формата укажите адрес или индекс, "
                "поставьте точку на карте и нажмите «Подтвердить точку»."
            )
        raise forms.ValidationError(
            "Подтвердите местоположение на карте (кнопка «Подтвердить точку»)."
        )


class OpportunitySubmissionForm(forms.ModelForm):
    class Meta:
        model = OpportunitySubmission
        fields = (
            "company_name", "title", "type", "format", "salary",
            "location", "postal_code", "description", "requirements",
            "skills_required", "expires_at",
        )
        widgets = {
            "company_name": forms.TextInput(attrs={"placeholder": "Название компании или организатора"}),
            "title": forms.TextInput(attrs={"placeholder": "Стажировка Python / IT-митап"}),
            "location": forms.TextInput(attrs={"placeholder": "Санкт-Петербург, Невский проспект, 28"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "123456"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Опишите возможность..."}),
            "requirements": forms.Textarea(attrs={"rows": 3, "placeholder": "Что нужно от участника..."}),
            "skills_required": forms.TextInput(attrs={"placeholder": "Python, SQL"}),
            "expires_at": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "company_name": "Компания / организатор",
            "title": "Название",
            "type": "Тип",
            "format": "Формат",
            "salary": "Зарплата / вознаграждение",
            "location": "Адрес",
            "postal_code": "Почтовый индекс",
            "description": "Описание",
            "requirements": "Требования",
            "skills_required": "Навыки",
            "expires_at": "Дата окончания",
        }

    def clean(self):
        cleaned = super().clean()
        _validate_map_location(self.data, cleaned)
        return cleaned


class CompanyContactPersonForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = (
            "contact_person_name",
            "contact_person_position",
            "contact_person_email",
            "contact_person_phone",
        )
        widgets = {
            "contact_person_name": forms.TextInput(attrs={"placeholder": "Анна Иванова", "class": "input-field"}),
            "contact_person_position": forms.TextInput(attrs={"placeholder": "HR-менеджер, рекрутер...", "class": "input-field"}),
            "contact_person_email": forms.EmailInput(attrs={"placeholder": "hr@company.ru", "class": "input-field"}),
            "contact_person_phone": forms.TextInput(attrs={"placeholder": "+7 (999) 123-45-67", "class": "input-field"}),
        }
        labels = {
            "contact_person_name": "ФИО",
            "contact_person_position": "Должность",
            "contact_person_email": "Email",
            "contact_person_phone": "Телефон",
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = (
            "cover_image_url", "tech_stack_json", "values_json", "perks_json",
            "linkedin_url", "telegram_url", "vk_url",
            "office_address", "founded_year", "team_size",
        )
        widgets = {
            "cover_image_url": forms.URLInput(attrs={"placeholder": "https://..."}),
            "tech_stack_json": forms.Textarea(attrs={"rows": 4, "placeholder": '{"Backend":["Go","Python"],"Frontend":["React","Next.js"]}'}),
            "values_json": forms.Textarea(attrs={"rows": 4, "placeholder": '[{"emoji":"🚀","title":"Скорость","desc":"Мы ценим быстрые решения"}]'}),
            "perks_json": forms.Textarea(attrs={"rows": 4, "placeholder": '[{"icon":"💻","title":"MacBook Pro"},{"icon":"🏥","title":"ДМС"}]'}),
            "linkedin_url": forms.URLInput(attrs={"placeholder": "https://linkedin.com/company/..."}),
            "telegram_url": forms.URLInput(attrs={"placeholder": "https://t.me/..."}),
            "vk_url": forms.URLInput(attrs={"placeholder": "https://vk.com/..."}),
            "office_address": forms.TextInput(attrs={"placeholder": "Москва, ул. Льва Толстого 16"}),
            "founded_year": forms.TextInput(attrs={"placeholder": "2012"}),
            "team_size": forms.TextInput(attrs={"placeholder": "500–1000 человек"}),
        }
        labels = {
            "cover_image_url": "URL обложки / фото офиса",
            "tech_stack_json": "Технологии (JSON)",
            "values_json": "Ценности (JSON)",
            "perks_json": "Преимущества (JSON)",
            "linkedin_url": "LinkedIn",
            "telegram_url": "Telegram",
            "vk_url": "ВКонтакте",
            "office_address": "Адрес офиса",
            "founded_year": "Год основания",
            "team_size": "Размер команды",
        }


class CompanyReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} ★") for i in range(1, 6)],
        label="Оценка",
        widget=forms.RadioSelect,
    )

    class Meta:
        model = CompanyReview
        fields = ("rating", "text", "vacancy_tag")
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "placeholder": "Поделитесь своим опытом работы с этой компанией..."}),
            "vacancy_tag": forms.TextInput(attrs={"placeholder": "Python Backend Developer (необязательно)"}),
        }
        labels = {
            "rating": "Оценка",
            "text": "Отзыв",
            "vacancy_tag": "Вакансия / позиция",
        }


class AvatarUploadForm(forms.ModelForm):
    avatar = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])],
        widget=forms.FileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
        label="Фото профиля",
    )

    class Meta:
        model = User
        fields = ("avatar",)

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            max_size = 2 * 1024 * 1024  # 2 MB
            if avatar.size > max_size:
                raise forms.ValidationError("Размер файла не должен превышать 2 МБ.")
        return avatar


class CuratorProfileForm(forms.ModelForm):
    """Форма редактирования профиля куратора/администратора."""
    display_name = forms.CharField(
        label="Отображаемое имя",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Иван Иванов"}),
    )

    class Meta:
        model = CuratorProfile
        fields = ("responsibility_area", "availability_schedule")
        widgets = {
            "responsibility_area": forms.TextInput(attrs={"placeholder": 'Web-разработка, гр. 422ISV-2'}),
            "availability_schedule": forms.TextInput(attrs={"placeholder": 'Будни, 10:00 - 18:00'}),
        }
        labels = {
            "responsibility_area": "Зона ответственности",
            "availability_schedule": "График доступности",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        if user:
            self.fields["display_name"].initial = user.display_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self._user and "display_name" in self.cleaned_data:
            self._user.display_name = self.cleaned_data["display_name"]
            if commit:
                self._user.save(update_fields=["display_name"])
        if commit:
            profile.save()
        return profile
