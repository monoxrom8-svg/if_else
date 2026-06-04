from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramplin', '0011_add_is_mentor_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mentor_status',
            field=models.CharField(
                choices=[('available', 'Доступен'), ('busy', 'Занят')],
                db_index=True,
                default='available',
                help_text='Автоматически переключается в «Занят» при 3 днях неактивности.',
                max_length=20,
                verbose_name='Статус ментора',
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='last_message_sent_at',
            field=models.DateTimeField(
                blank=True,
                help_text='Обновляется автоматически при каждой отправке сообщения ментором.',
                null=True,
                verbose_name='Последнее сообщение отправлено',
            ),
        ),
    ]
