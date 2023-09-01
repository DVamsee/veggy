# Generated by Django 4.1.5 on 2023-01-22 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('profiles', '0003_qr_key_qr_qr_delete_qr_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qr_login',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('key', models.CharField(default='0', max_length=64)),
                ('qr', models.ImageField(default='dumm', upload_to='qr/')),
            ],
        ),
    ]