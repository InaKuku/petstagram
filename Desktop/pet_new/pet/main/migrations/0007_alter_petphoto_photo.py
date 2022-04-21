# Generated by Django 4.0.3 on 2022-04-02 18:36

from django.db import migrations, models
import pet.common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petphoto',
            name='photo',
            field=models.ImageField(upload_to='', validators=[pet.common.validators.MaxFileSizeInMbValidator(5)]),
        ),
    ]