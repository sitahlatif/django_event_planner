# Generated by Django 2.1 on 2019-02-28 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_events_pretty_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='pretty_picture',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]