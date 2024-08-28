# Generated by Django 4.2.13 on 2024-08-28 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topFive', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='away_team_free_throws',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='away_team_three_pointers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='away_team_two_pointers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='home_team_free_throws',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='home_team_three_pointers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='home_team_two_pointers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='result',
            field=models.CharField(blank=True, default='Not Played', max_length=50),
        ),
    ]
