# Generated by Django 5.0.1 on 2025-06-29 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='currency',
            field=models.CharField(default='USD', help_text='Currency code (e.g., USD, EUR, RP)', max_length=3),
        ),
    ]
