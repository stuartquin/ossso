# Generated by Django 3.2.7 on 2021-11-20 10:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0003_samlresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedirectURI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('uri', models.CharField(max_length=2048)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sso.organization')),
            ],
        ),
    ]