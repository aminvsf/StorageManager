# Generated by Django 4.0.1 on 2022-01-25 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_remove_store_temp1_remove_store_temp2'),
        ('bills', '0004_remove_outputdetail_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store', verbose_name='انبار'),
        ),
        migrations.AlterField(
            model_name='output',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store', verbose_name='انبار'),
        ),
    ]
