# Generated by Django 5.1.3 on 2024-11-28 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
