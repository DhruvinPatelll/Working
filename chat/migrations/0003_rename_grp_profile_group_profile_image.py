# Generated by Django 5.0.4 on 2024-05-06 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_group_grp_profile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="group",
            old_name="grp_profile",
            new_name="profile_image",
        ),
    ]
