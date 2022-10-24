# Generated by Django 4.0.6 on 2022-10-21 19:29

from django.db import migrations, models
import libraryapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0003_userprofile_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='end_date',
            field=models.DateField(default=libraryapp.models.get_expiry, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='fine',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='request',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]