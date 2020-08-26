# Generated by Django 3.1 on 2020-08-26 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0010_auto_20200825_2359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantToInterview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.interview')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.participant')),
            ],
        ),
        migrations.AddField(
            model_name='interview',
            name='participant',
            field=models.ManyToManyField(related_name='interviews', through='core.ParticipantToInterview', to='core.Participant'),
        ),
    ]