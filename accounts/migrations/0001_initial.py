# Generated by Django 4.1.1 on 2022-11-15 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.CharField(choices=[('admin', 'admin'), ('leader', 'leader'), ('worker', 'worker')], default='worker', max_length=100)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users List',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('fathers_name', models.CharField(max_length=255)),
                ('mothers_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('sex_name', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Others')], max_length=55)),
                ('phone', models.CharField(max_length=14)),
                ('postel_code', models.CharField(max_length=14)),
                ('nid_card_no', models.CharField(max_length=14)),
                ('city', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=300)),
                ('nationality', models.CharField(max_length=55)),
                ('marital_Status', models.BooleanField(default=False)),
                ('employe_image', models.ImageField(upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users Profiles',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('is_seen', models.BooleanField(default=False)),
                ('message', models.TextField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('from_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_admin', to=settings.AUTH_USER_MODEL)),
                ('from_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_leader', to=settings.AUTH_USER_MODEL)),
                ('to_leader', models.ManyToManyField(blank=True, related_name='to_leader', to=settings.AUTH_USER_MODEL)),
                ('to_worker', models.ManyToManyField(blank=True, related_name='to_worker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_acc_num', models.CharField(max_length=255)),
                ('acc_holder_name', models.CharField(max_length=255)),
                ('acc_branch_name', models.CharField(max_length=255)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bank', to='accounts.profile')),
            ],
            options={
                'verbose_name_plural': 'Users Bank Info',
            },
        ),
    ]