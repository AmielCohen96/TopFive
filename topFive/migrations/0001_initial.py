# Generated by Django 5.1 on 2024-08-25 18:27

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import topFive.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('defense', models.IntegerField(default=topFive.models.get_default_defense)),
                ('offense', models.IntegerField(default=topFive.models.get_default_offense)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(default=topFive.models.get_default_age)),
                ('height', models.FloatField(default=topFive.models.get_default_height)),
                ('position', models.IntegerField(default=topFive.models.get_default_position)),
                ('speed', models.IntegerField(default=topFive.models.get_default_stat)),
                ('strength', models.IntegerField(default=topFive.models.get_default_stat)),
                ('stamina', models.IntegerField(default=topFive.models.get_default_stat)),
                ('shooting3', models.IntegerField(default=topFive.models.get_default_stat)),
                ('shooting2', models.IntegerField(default=topFive.models.get_default_stat)),
                ('jumping', models.IntegerField(default=topFive.models.get_default_stat)),
                ('defense', models.IntegerField(default=topFive.models.get_default_stat)),
                ('rating', models.IntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('team_name', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Custom User',
                'verbose_name_plural': 'Custom Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('level', models.IntegerField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='customuser_set', related_query_name='customuser', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', related_query_name='customuser', to='auth.permission')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('full_name', models.CharField(max_length=100)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
                ('budget', models.IntegerField(default=1000000)),
                ('points', models.IntegerField(default=0)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('average_rating', models.IntegerField(default=0)),
                ('arena', models.CharField(max_length=100)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='topFive.coach')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topFive.league')),
                ('players', models.ManyToManyField(blank=True, related_name='teams', to='topFive.player')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='topFive.team'),
        ),
        migrations.AddField(
            model_name='league',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='leagues', to='topFive.team'),
        ),
    ]
