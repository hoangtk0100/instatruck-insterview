# Generated by Django 3.2.20 on 2023-08-29 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100, null=True)),
                ('place', models.CharField(max_length=500, null=True)),
                ('masterpiece', models.CharField(max_length=500, null=True)),
                ('award_win', models.IntegerField(blank=True, default=None, null=True)),
                ('award_nom', models.IntegerField(blank=True, default=None, null=True)),
                ('person_link', models.URLField(default=None, max_length=500, null=True)),
                ('award_link', models.URLField(default=None, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100, null=True)),
                ('place', models.CharField(max_length=500, null=True)),
                ('masterpiece', models.CharField(max_length=500, null=True)),
                ('award_win', models.IntegerField(blank=True, default=None, null=True)),
                ('award_nom', models.IntegerField(blank=True, default=None, null=True)),
                ('person_link', models.URLField(default=None, max_length=500, null=True)),
                ('award_link', models.URLField(default=None, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=500, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('genres', models.CharField(max_length=100)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('metascore', models.IntegerField(blank=True, default=None, null=True)),
                ('votes', models.IntegerField(blank=True, null=True)),
                ('gross_earning_in_mil', models.FloatField(blank=True, default=None, null=True)),
                ('actor', models.ForeignKey(blank=True, db_column='actor_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_fk_actor', to='pages.actor')),
                ('director', models.ForeignKey(blank=True, db_column='director_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_fk_director', to='pages.director')),
            ],
        ),
    ]
