# Generated by Django 4.2.7 on 2023-12-30 16:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('idAlbum', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('idGenero', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idUsuario', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('opinion', models.TextField(blank=True, max_length=1000)),
                ('idAlbum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.album')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='generos',
            field=models.ManyToManyField(to='main.genero'),
        ),
    ]
