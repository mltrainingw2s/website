# Generated by Django 3.2.10 on 2022-01-21 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_auto_20220121_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restmlimage',
            name='smile_percentage',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='restmlwebcam',
            name='smile_percentage',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
