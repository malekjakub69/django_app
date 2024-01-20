# Generated by Django 5.0.1 on 2024-01-19 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazev', models.CharField(max_length=255)),
                ('zobrazit', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hodnota', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obrazek', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazev', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('cena', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mena', models.CharField(max_length=3)),
                ('published_on', models.DateTimeField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazev_atributu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_app.attributename')),
                ('hodnota_atributu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_app.attributevalue')),
            ],
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazev', models.CharField(max_length=255)),
                ('attributes', models.ManyToManyField(to='django_app.attribute')),
                ('obrazek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_app.image')),
                ('products', models.ManyToManyField(to='django_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_app.attribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazev', models.CharField(max_length=255)),
                ('obrazek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_app.image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_app.product')),
            ],
        ),
    ]