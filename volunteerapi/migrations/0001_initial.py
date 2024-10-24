# Generated by Django 4.2.16 on 2024-10-24 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=800)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VolunteerOpportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='volunteerapi.opportunity')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volunteers', to='volunteerapi.volunteer')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer_Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteerapi.skill')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteerapi.volunteer')),
            ],
        ),
        migrations.AddField(
            model_name='volunteer',
            name='skills',
            field=models.ManyToManyField(related_name='volunteers', through='volunteerapi.Volunteer_Skill', to='volunteerapi.skill'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='volunteer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=400)),
                ('location', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opportunity_Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteerapi.opportunity')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteerapi.skill')),
            ],
        ),
        migrations.AddField(
            model_name='opportunity',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='volunteerapi.organization'),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='skills',
            field=models.ManyToManyField(related_name='opportunities', through='volunteerapi.Opportunity_Skill', to='volunteerapi.skill'),
        ),
    ]
