# Generated by Django 4.2.5 on 2023-09-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('desc', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')], max_length=50)),
                ('target_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]