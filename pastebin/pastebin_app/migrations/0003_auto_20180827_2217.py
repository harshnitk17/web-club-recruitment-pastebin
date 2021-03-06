# Generated by Django 2.0.6 on 2018-08-27 16:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pastebin_app', '0002_editinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='editinfo',
            name='data_title',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='editinfo',
            name='syntax',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='editinfo',
            name='share_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
