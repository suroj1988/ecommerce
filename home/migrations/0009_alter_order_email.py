# Generated by Django 5.0.2 on 2024-03-03 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_cart_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]
