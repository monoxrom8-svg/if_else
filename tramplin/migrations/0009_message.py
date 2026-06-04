import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramplin', '0008_contact_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Текст')),
                ('file_attachment', models.FileField(blank=True, null=True, upload_to='chat_attachments/%Y/%m/', verbose_name='Вложение')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='messages_sent',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('receiver', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='messages_received',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
