# Generated by Django 4.2.18 on 2025-01-30 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="junction", old_name="location", new_name="City",
        ),
        migrations.RemoveField(model_name="junction", name="city",),
        migrations.AlterField(
            model_name="junction", name="name", field=models.CharField(max_length=255),
        ),
    ]
