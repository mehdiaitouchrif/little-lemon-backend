# Generated by Django 4.2.1 on 2023-05-30 22:08

from django.db import migrations, models
import django.db.models.deletion
import littlelemonapi.validators


class Migration(migrations.Migration):

    dependencies = [
        ('littlelemonapi', '0002_reservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='restaurant/images', validators=[littlelemonapi.validators.validate_file_size])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='littlelemonapi.menuitem')),
            ],
        ),
    ]
