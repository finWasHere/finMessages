# Generated by Django 4.0.6 on 2022-07-30 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messageapi', '0003_alter_message_received'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='sent',
        ),
    ]