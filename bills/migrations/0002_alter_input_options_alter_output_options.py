# Generated by Django 4.0.1 on 2022-01-23 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='input',
            options={'ordering': ['-timestamp'], 'verbose_name': 'حواله ورود', 'verbose_name_plural': 'حواله های ورود'},
        ),
        migrations.AlterModelOptions(
            name='output',
            options={'ordering': ['-timestamp'], 'verbose_name': 'حواله خروج', 'verbose_name_plural': 'حواله های خروج'},
        ),
    ]
