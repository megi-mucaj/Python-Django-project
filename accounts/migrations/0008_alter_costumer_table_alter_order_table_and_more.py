# Generated by Django 4.0.2 on 2022-03-14 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_product_description'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='costumer',
            table='costumer',
        ),
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
        migrations.AlterModelTable(
            name='product',
            table='product',
        ),
        migrations.AlterModelTable(
            name='tag',
            table='tag',
        ),
    ]