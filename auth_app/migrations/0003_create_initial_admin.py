from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_initial_superuser(apps, schema_editor):
    """Create an initial superuser with username 'CoderrAdmin' and type 'business'."""
    User = apps.get_model('auth', 'User')
    CustomUser = apps.get_model('auth_app', 'CustomUser')
    if not User.objects.filter(username='CoderrAdmin').exists():
        user = User.objects.create(
            username='CoderrAdmin',
            email='admin@example.com',
            is_staff=True,
            is_superuser=True,
            password=make_password('CoderrAdmin123!'),
        )
        CustomUser.objects.create(
            id=user.id, 
            user=user,
            type='business'
        )


def create_demo_customer(apps, schema_editor):
    """Create a demo customer user with username 'DemoCustomer' and type 'customer'."""
    User = apps.get_model('auth', 'User')
    CustomUser = apps.get_model('auth_app', 'CustomUser')
    if not User.objects.filter(username='DemoCustomer').exists():
        user = User.objects.create(
            username='DemoCustomer',
            email='customer@demo.de',
            is_staff=False,
            is_superuser=False,
            password=make_password('C-D3mo-P4ssw0rd'),
        )
        CustomUser.objects.create(
            id=user.id, 
            user=user,
            type='customer'
        )


def create_demo_business(apps, schema_editor):
    """Create a demo business user with username 'DemoBusiness' and type 'business'."""
    User = apps.get_model('auth', 'User')
    CustomUser = apps.get_model('auth_app', 'CustomUser')
    if not User.objects.filter(username='DemoBusiness').exists():
        user = User.objects.create(
            username='DemoBusiness',
            email='business@demo.de',
            is_staff=False,
            is_superuser=False,
            password=make_password('B-D3mo-P4ssw0rd'),
        )
        CustomUser.objects.create(
            id=user.id, 
            user=user,
            type='business'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_alter_customuser_description_alter_customuser_file_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_superuser),
        migrations.RunPython(create_demo_customer),
        migrations.RunPython(create_demo_business),
    ]