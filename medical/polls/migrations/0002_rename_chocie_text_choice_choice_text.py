# Generated by Django 4.1.6 on 2023-02-01 14:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="choice",
            old_name="chocie_text",
            new_name="choice_text",
        ),
    ]
