# Generated by Django 4.0.1 on 2022-01-18 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(default='temp', max_length=30, verbose_name='عنوان'),
            preserve_default=False,
        ),
    ]
