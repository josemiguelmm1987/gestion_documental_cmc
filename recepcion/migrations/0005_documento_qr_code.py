# Generated by Django 5.1.6 on 2025-02-23 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recepcion', '0004_documento_observaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/', verbose_name='Código QR'),
        ),
    ]
