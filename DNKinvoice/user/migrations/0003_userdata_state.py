# Generated by Django 5.0 on 2023-12-24 14:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_user_details_userdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='state',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
