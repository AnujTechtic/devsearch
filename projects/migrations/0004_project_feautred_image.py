# Generated by Django 4.2.10 on 2024-02-14 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_rename_name_tag_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='feautred_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
