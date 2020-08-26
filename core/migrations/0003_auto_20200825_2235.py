# Generated by Django 3.1 on 2020-08-25 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20200825_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
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
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
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