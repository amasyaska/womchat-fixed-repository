# Generated by Django 5.0.4 on 2024-04-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_chat_instantmessage_usertochat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='title',
            field=models.CharField(default='aaa', max_length=255),
            preserve_default=False,
        ),
    ]
