# Generated by Django 2.1 on 2019-02-27 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20190226_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='pretty_picture',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]