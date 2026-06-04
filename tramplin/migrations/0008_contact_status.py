from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramplin', '0007_add_coordinates_to_opportunity_and_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.CharField(
                choices=[('pending', 'Ожидает подтверждения'), ('accepted', 'Принят')],
                default='accepted',  # existing rows are already accepted
                max_length=10,
            ),
        ),
    ]
