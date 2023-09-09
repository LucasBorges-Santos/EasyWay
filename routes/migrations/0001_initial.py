# Generated by Django 4.1.5 on 2023-09-03 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PointLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(max_length=100)),
                ('longitude', models.FloatField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RouteLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_locations_as_final_point', to='routes.pointlocation')),
                ('initial_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_locations_as_initial_point', to='routes.pointlocation')),
            ],
        ),
        migrations.CreateModel(
            name='SpaceRoutes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routes', models.ManyToManyField(related_name='space_routes_as_route_locations', to='routes.routelocation')),
            ],
        ),
    ]
