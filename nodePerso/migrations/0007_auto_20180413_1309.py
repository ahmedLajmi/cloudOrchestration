# Generated by Django 2.0.3 on 2018-04-13 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nodePerso', '0006_auto_20180412_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodepersonalised',
            name='compute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='createTemplate.Compute'),
        ),
        migrations.AlterField(
            model_name='nodepersonalised',
            name='database',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='createTemplate.Database'),
        ),
        migrations.AlterField(
            model_name='nodepersonalised',
            name='softwareComponent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='createTemplate.SoftwareComponent'),
        ),
        migrations.AlterField(
            model_name='nodepersonalised',
            name='webApplication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='createTemplate.WebApplication'),
        ),
        migrations.AlterField(
            model_name='nodepersonalised',
            name='webServer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='createTemplate.WebServer'),
        ),
    ]