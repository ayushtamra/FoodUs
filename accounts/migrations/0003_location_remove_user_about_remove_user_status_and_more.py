# Generated by Django 4.0.2 on 2022-08-05 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('LocationId', models.AutoField(primary_key=True, serialize=False)),
                ('LocationName', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='about',
        ),
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False, verbose_name='customer status'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_restaurant_owner',
            field=models.BooleanField(default=False, verbose_name='restaurant owner status'),
        ),
        migrations.CreateModel(
            name='RestaurantOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10)),
                ('addressline1', models.TextField(max_length=20)),
                ('addressline2', models.TextField(max_length=20)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10)),
                ('addressline1', models.TextField(max_length=20)),
                ('addressline2', models.TextField(max_length=20)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
