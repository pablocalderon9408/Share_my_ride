# Generated by Django 3.2.18 on 2023-02-24 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('circles', '0002_auto_20230220_0124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('code', models.CharField(blank=True, max_length=50, unique=True, verbose_name='invitation code')),
                ('used', models.BooleanField(default=False, help_text='Set to true when the invitation is used.', verbose_name='used')),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('circle', models.ForeignKey(help_text='Circle to which the invitation belongs.', on_delete=django.db.models.deletion.CASCADE, to='circles.circle')),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issued_by', to=settings.AUTH_USER_MODEL)),
                ('used_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='used_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-used', '-created'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
