# Generated by Django 5.0.4 on 2024-04-16 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_exp_date_alter_user_refresh_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='refresh_token',
            field=models.UUIDField(null=True),
        ),
    ]
