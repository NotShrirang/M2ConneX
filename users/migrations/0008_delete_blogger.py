# Generated by Django 4.2.7 on 2023-12-28 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_alumniportaluser_profilepicture'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blogger',
        ),
    ]