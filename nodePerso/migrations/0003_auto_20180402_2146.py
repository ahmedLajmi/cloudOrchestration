# Generated by Django 2.0.3 on 2018-04-02 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nodePerso', '0002_auto_20180402_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodepersonalised',
            name='derivedFrom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='nodePerso.BaseNode', verbose_name='Derived From'),
        ),
    ]