# Generated by Django 3.1.6 on 2021-02-15 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Law',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, max_length=150, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteLaw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('law', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='law.law')),
            ],
        ),
    ]
