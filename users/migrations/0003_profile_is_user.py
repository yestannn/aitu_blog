# Generated by Django 3.0.7 on 2020-07-10 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200627_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_user',
            field=models.CharField(choices=[('student', 'student'), ('teacher', 'teacher'), ('club', 'club')], default='student', max_length=7),
        ),
    ]
