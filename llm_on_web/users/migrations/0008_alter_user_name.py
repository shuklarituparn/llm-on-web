# Generated by Django 4.2.13 on 2024-06-23 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Name of User"
            ),
        ),
    ]
