# Generated by Django 4.0.3 on 2022-04-21 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_petphoto_likes_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='pet',
        ),
        migrations.AddField(
            model_name='like',
            name='pet_photo',
            field=models.ForeignKey(default='5', on_delete=django.db.models.deletion.CASCADE, to='main.petphoto'),
            preserve_default=False,
        ),
    ]
