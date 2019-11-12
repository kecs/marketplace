# Generated by Django 2.2.6 on 2019-11-12 16:24

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20191112_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auction',
            name='img1',
            field=models.ImageField(upload_to=main_app.models.get_upload_to_path),
        ),
    ]