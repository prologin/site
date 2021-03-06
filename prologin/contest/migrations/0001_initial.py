# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.conf import settings
from django.db import models, migrations

import contest.models
import prologin.models

try:
    from jsonfield import JSONField
except ImportError:
    from django.contrib.postgres.fields.jsonb import JSONField


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shirt_size', prologin.models.EnumField(contest.models.ShirtSize, null=True, blank=True, choices=[(0, 'XS'), (1, 'S'), (2, 'M'), (3, 'L'), (4, 'XL'), (5, 'XXL')], db_index=True, help_text='We usually provide unisex Prologin t-shirts to the finalists.', verbose_name='T-shirt size')),
                ('preferred_language', prologin.models.CodingLanguageField(null=True, choices=[('ada', 'Ada'), ('brainfuck', 'Brainfuck'), ('c', 'C'), ('csharp', 'C#'), ('cpp', 'C++'), ('fsharp', 'F#'), ('haskell', 'Haskell'), ('java', 'Java'), ('js', 'Javascript'), ('lua', 'Lua'), ('ocaml', 'OCaml'), ('pascal', 'Pascal'), ('perl', 'Perl'), ('php', 'PHP'), ('pseudocode', 'Pseudocode'), ('python2', 'Python 2'), ('python3', 'Python 3'), ('scheme', 'Scheme'), ('vb', 'VB')], verbose_name='Coding language', max_length=64, blank=True, db_index=True, help_text='The programming language you will most likely use during the regional events.')),
                ('score_qualif_qcm', models.IntegerField(verbose_name='Quiz score', null=True, blank=True)),
                ('score_qualif_algo', models.IntegerField(verbose_name='Algo exercises score', null=True, blank=True)),
                ('score_qualif_bonus', models.IntegerField(verbose_name='Bonus score', null=True, blank=True)),
                ('score_semifinal_written', models.IntegerField(verbose_name='Written exam score', null=True, blank=True)),
                ('score_semifinal_interview', models.IntegerField(verbose_name='Interview score', null=True, blank=True)),
                ('score_semifinal_machine', models.IntegerField(verbose_name='Machine exam score', null=True, blank=True)),
                ('score_semifinal_bonus', models.IntegerField(verbose_name='Bonus score', null=True, blank=True)),
                ('score_final', models.IntegerField(verbose_name='Score', null=True, blank=True)),
                ('score_final_bonus', models.IntegerField(verbose_name='Bonus score', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('year', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('date_begin', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
            ],
            options={
                'ordering': ('-year',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', prologin.models.EnumField(contest.models.Event.Type, choices=[(0, 'Qualification'), (1, 'Regional event'), (2, 'Final')], db_index=True)),
                ('date_begin', models.DateTimeField(null=True, blank=True)),
                ('date_end', models.DateTimeField(null=True, blank=True)),
                ('center', models.ForeignKey(null=True, to='centers.Center', related_name='events', blank=True, on_delete=models.SET_NULL)),
                ('edition', models.ForeignKey(related_name='events', to='contest.Edition', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='EventWish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(editable=False, db_index=True)),
                ('contestant', models.ForeignKey(to='contest.Contestant', on_delete=models.CASCADE)),
                ('event', models.ForeignKey(to='contest.Event', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contestant',
            name='edition',
            field=models.ForeignKey(related_name='contestants', to='contest.Edition', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='contestant',
            name='event_wishes',
            field=models.ManyToManyField(blank=True, through='contest.EventWish', related_name='applicants', to='contest.Event', verbose_name='Regional event assignation whishes'),
        ),
        migrations.AddField(
            model_name='contestant',
            name='user',
            field=models.ForeignKey(related_name='contestants', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together={('user', 'edition')},
        ),
        migrations.CreateModel(
            name='ContestantCorrection',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('comment', models.TextField(blank=True)),
                ('event_type', prologin.models.EnumField(contest.models.Event.Type, choices=[(0, 'Qualification'), (1, 'Regional event'), (2, 'Final')], db_index=True)),
                ('changes', JSONField(blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(related_name='contestant_correction', to=settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)),
                ('contestant', models.ForeignKey(to='contest.Contestant', related_name='corrections', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='contestant',
            name='assigned_event',
            field=models.ForeignKey(null=True, to='contest.Event', blank=True, related_name='assigned_contestants', verbose_name='Regional event assigned event', on_delete=models.SET_NULL),
        ),
    ]
