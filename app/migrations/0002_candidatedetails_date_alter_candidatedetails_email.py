# Generated by Django 4.1.3 on 2023-01-10 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatedetails',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='candidatedetails',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
