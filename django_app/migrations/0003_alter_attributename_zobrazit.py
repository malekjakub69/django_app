# Generated by Django 5.0.1 on 2024-01-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0002_alter_attributename_nazev_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributename',
            name='zobrazit',
            field=models.BooleanField(null=True),
        ),
    ]