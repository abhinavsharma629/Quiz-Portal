# Generated by Django 2.1.5 on 2019-02-03 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizportal', '0002_solved1'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolvedQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('q_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizportal.QuestionData')),
            ],
        ),
        migrations.RemoveField(
            model_name='solved',
            name='id_no',
        ),
        migrations.RemoveField(
            model_name='solved',
            name='q_id',
        ),
        migrations.RemoveField(
            model_name='solved1',
            name='id_no',
        ),
        migrations.RemoveField(
            model_name='solved1',
            name='q_id',
        ),
        migrations.DeleteModel(
            name='Solved',
        ),
        migrations.DeleteModel(
            name='Solved1',
        ),
    ]