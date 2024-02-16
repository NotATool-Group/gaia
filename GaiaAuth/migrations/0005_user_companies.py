# Generated by Django 5.0.1 on 2024-02-16 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("GaiaAuth", "0004_passwordreset"),
        ("GaiaCompany", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="companies",
            field=models.ManyToManyField(blank=True, related_name="users", to="GaiaCompany.company"),
        ),
    ]