# Generated by Django 3.1 on 2020-08-25 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200825_2259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participanttointerview',
            name='interview',
        ),
        migrations.RemoveField(
            model_name='participanttointerview',
            name='participant',
        ),
        migrations.DeleteModel(
            name='Interview',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.DeleteModel(
            name='ParticipantToInterview',
        ),
    ]