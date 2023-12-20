# Generated by Django 4.2.7 on 2023-12-20 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_remove_useranalytics_visitcount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranalytics',
            name='analyticsType',
            field=models.CharField(choices=[('profile visit', 'profile visit'), ('profile search', 'profile search'), ('feed like', 'feed like'), ('feed comment', 'feed comment'), ('feed share', 'feed share'), ('connection', 'connection')], default='profile visit', max_length=50),
        ),
    ]
