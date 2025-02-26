# Generated by Django 4.2.17 on 2025-02-24 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipper_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_person', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('mobile_number', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_name', models.CharField(max_length=100)),
                ('receiver_address', models.TextField()),
                ('receiver_country', models.CharField(max_length=50)),
                ('receiver_city', models.CharField(max_length=50)),
                ('receiver_location', models.CharField(blank=True, max_length=100, null=True)),
                ('receiver_contact_person', models.CharField(max_length=100)),
                ('receiver_contact_number', models.CharField(max_length=20)),
                ('receiver_mobile_number', models.CharField(blank=True, max_length=20, null=True)),
                ('awb_number', models.CharField(max_length=50, unique=True)),
                ('reference_number', models.CharField(blank=True, max_length=50, null=True)),
                ('booking_date', models.DateField()),
                ('booking_time', models.TimeField()),
                ('product_type', models.CharField(max_length=50)),
                ('pieces', models.PositiveIntegerField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('v_weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('c_weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_description', models.TextField()),
                ('special_instruction', models.TextField(blank=True, null=True)),
                ('cod_amount', models.DecimalField(decimal_places=2, help_text='COD in AED', max_digits=10)),
                ('base_price', models.DecimalField(decimal_places=2, help_text='Base shipping cost', max_digits=10)),
                ('additional_charges', models.DecimalField(decimal_places=2, default=0.0, help_text='Additional fees', max_digits=10)),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipments', to='shipments.shipper')),
            ],
        ),
    ]
