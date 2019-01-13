# Generated by Django 2.1.5 on 2019-01-13 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.IntegerField()),
                ('job', models.CharField(choices=[('T', 'Taker'), ('R', 'Rider')], max_length=1)),
                ('image', models.ImageField(upload_to='titles')),
            ],
        ),
    ]
