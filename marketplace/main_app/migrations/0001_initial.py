# Generated by Django 2.2.6 on 2019-11-11 20:10

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketplaceUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('did_accept_tos', models.BooleanField(blank=True, default=False)),
                ('member_since', models.DateField(auto_now_add=True)),
                ('address', models.CharField(max_length=1024)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('product_condition', models.IntegerField(choices=[(1, 'New'), (2, 'Excellent'), (3, 'Used'), (4, 'As pictured')], default=1)),
                ('duration', models.IntegerField(choices=[(30, 'One month'), (60, 'Two month'), (15, 'One week')], default=30)),
                ('starting_price', models.IntegerField()),
                ('actual_price', models.IntegerField()),
                ('start_date', models.DateField()),
                ('img1', models.ImageField(upload_to=main_app.models.get_upload_to_path)),
                ('img2', models.ImageField(upload_to=main_app.models.get_upload_to_path)),
                ('img3', models.ImageField(upload_to=main_app.models.get_upload_to_path)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TermsOfUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Auction')),
                ('marketplaceuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('review', models.TextField(blank=True, default='')),
                ('auction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Auction')),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_by_seller', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewed_by_buyer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Auction')),
                ('marketplaceuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='auction',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Brand'),
        ),
        migrations.AddField(
            model_name='auction',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.City'),
        ),
        migrations.AddField(
            model_name='auction',
            name='highest_bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='highest_bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auction',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='marketplaceuser',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.City'),
        ),
        migrations.AddField(
            model_name='marketplaceuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='marketplaceuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
