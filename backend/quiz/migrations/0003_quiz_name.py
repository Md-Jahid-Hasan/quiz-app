# Generated by Django 4.1.5 on 2023-01-21 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_remove_question_option1_remove_question_option2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]