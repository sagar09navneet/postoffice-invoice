# Generated by Django 4.2.9 on 2024-02-06 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_userdata_bill_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='bill_id',
            field=models.CharField(max_length=50),
        ),
    ]
