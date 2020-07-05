# Generated by Django 2.2.7 on 2020-06-14 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paipage', '0003_auto_20200611_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsetting',
            name='updated_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
