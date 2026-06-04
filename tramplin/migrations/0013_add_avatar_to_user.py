from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tramplin", "0012_mentor_status_and_activity"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="avatars/",
                verbose_name="Фото профиля",
            ),
        ),
    ]
