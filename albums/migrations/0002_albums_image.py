# Generated by Django 5.0.1 on 2024-01-16 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='albums',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='album_images/'),
        ),
    ]
