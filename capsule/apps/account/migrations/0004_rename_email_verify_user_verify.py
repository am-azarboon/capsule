# Generated by Django 4.2.4 on 2023-08-29 20:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_user_email_verify_alter_user_full_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="email_verify",
            new_name="verify",
        ),
    ]