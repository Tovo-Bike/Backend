# Generated by Django 2.1.5 on 2019-01-13 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longtitude', models.DecimalField(decimal_places=3, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=3, max_digits=9)),
                ('description', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(max_length=128)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart_lon', models.DecimalField(decimal_places=6, max_digits=9)),
                ('depart_lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('dest_lon', models.DecimalField(decimal_places=6, max_digits=9)),
                ('dest_lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('taker_score', models.IntegerField(default=0)),
                ('rider_score', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(null=True)),
                ('arrival_time', models.DateTimeField(null=True)),
            ],
        ),
    ]
