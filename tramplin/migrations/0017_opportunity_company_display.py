from django.db import migrations, models


def ensure_company_display_column(apps, schema_editor):
    """Колонка могла появиться из SQL-дампа без default — выравниваем схему."""
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*) FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'tramplin_opportunity'
              AND COLUMN_NAME = 'company_display'
            """
        )
        exists = cursor.fetchone()[0]
        if not exists:
            cursor.execute(
                """
                ALTER TABLE tramplin_opportunity
                ADD COLUMN company_display varchar(200) NOT NULL DEFAULT ''
                """
            )
        else:
            cursor.execute(
                """
                ALTER TABLE tramplin_opportunity
                MODIFY company_display varchar(200) NOT NULL DEFAULT ''
                """
            )
        cursor.execute(
            """
            UPDATE tramplin_opportunity o
            INNER JOIN tramplin_user u ON o.employer_id = u.id
            SET o.company_display = LEFT(
                COALESCE(NULLIF(TRIM(u.company_name), ''), u.display_name, u.username, ''),
                200
            )
            WHERE o.company_display = '' OR o.company_display IS NULL
            """
        )


class Migration(migrations.Migration):

    dependencies = [
        ("tramplin", "0016_opportunity_submissions_and_postal"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name="opportunity",
                    name="company_display",
                    field=models.CharField(
                        blank=True,
                        default="",
                        max_length=200,
                        verbose_name="Компания (отображение)",
                    ),
                ),
            ],
            database_operations=[
                migrations.RunPython(ensure_company_display_column, migrations.RunPython.noop),
            ],
        ),
    ]
