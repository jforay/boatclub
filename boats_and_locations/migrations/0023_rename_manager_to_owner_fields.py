from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boats_and_locations', '0022_add_marina_manager_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marina',
            old_name='manager_name',
            new_name='owner_name',
        ),
        migrations.RenameField(
            model_name='marina',
            old_name='manager_phone',
            new_name='owner_phone',
        ),
        migrations.RenameField(
            model_name='marina',
            old_name='manager_email',
            new_name='owner_email',
        ),
    ]
