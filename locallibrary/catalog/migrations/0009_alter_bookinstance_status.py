# Generated by Django 5.1.2 on 2024-11-06 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_bookinstance_borrower_alter_bookinstance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'На обслуживании'), ('o', 'В займе'), ('a', 'Доступно'), ('r', 'Зарезервировано')], default='m', help_text='Book availability', max_length=1),
        ),
    ]
