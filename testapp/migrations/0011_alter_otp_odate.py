# Generated by Django 3.2.2 on 2021-06-21 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0010_otp_otp_validated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='odate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
