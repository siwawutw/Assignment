# Generated by Django 3.1.13 on 2021-11-20 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog',
            new_name='Blogs',
        ),
    ]
