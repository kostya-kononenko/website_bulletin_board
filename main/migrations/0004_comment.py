# Generated by Django 4.1.4 on 2022-12-16 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_bb_additionalimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30, verbose_name='Автор')),
                ('content', models.TextField(verbose_name='Зміст')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Виводити на екран')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубліковано')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bb', verbose_name='Оголошення')),
            ],
            options={
                'verbose_name': 'Коментарі',
                'verbose_name_plural': 'Коментарі',
                'ordering': ['created_at'],
            },
        ),
    ]
