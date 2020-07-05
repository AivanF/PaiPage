# Generated by Django 2.2.7 on 2020-05-19 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paipage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='layout',
            field=models.CharField(default='lo-menu-left', max_length=256),
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=models.CharField(default='pg-usual', max_length=256),
        ),
        migrations.AlterField(
            model_name='page',
            name='upper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='paipage.Page'),
        ),
        migrations.AlterField(
            model_name='pagetext',
            name='language',
            field=models.CharField(choices=[('_', 'NoLang'), ('en', 'English'), ('ru', 'Русский')], max_length=16),
        ),
        migrations.AlterUniqueTogether(
            name='pagetext',
            unique_together={('page', 'language')},
        ),
    ]
