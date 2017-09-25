# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-10 17:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membership',
            name='roles',
            field=models.ManyToManyField(related_name='memberships', to='groups.Role'),
        ),
        migrations.AddField(
            model_name='invite',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to='groups.Group'),
        ),
        migrations.AddField(
            model_name='invite',
            name='invited',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_invitations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invite',
            name='inviter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_invites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='memberships',
            field=models.ManyToManyField(through='groups.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
