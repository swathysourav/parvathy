# Generated by Django 4.2.10 on 2024-02-24 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_alter_reviewrating_movie_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='movie_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movie.post'),
        ),
    ]
