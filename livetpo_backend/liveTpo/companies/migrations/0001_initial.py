# Generated by Django 4.2.2 on 2025-04-22 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('job_roles', models.JSONField(default=list)),
                ('ctc', models.CharField(blank=True, max_length=255, null=True)),
                ('eligibility_cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('eligibility_skills', models.JSONField(default=list)),
                ('mode_of_work', models.CharField(choices=[('remote', 'Remote'), ('onsite', 'Onsite'), ('hybrid', 'Hybrid')], default='remote', max_length=50)),
                ('bond', models.TextField(blank=True, null=True)),
                ('selection_process', models.TextField(blank=True, null=True)),
                ('openings', models.PositiveIntegerField(default=0)),
                ('perks', models.TextField(blank=True, null=True)),
                ('pdfs', models.FileField(blank=True, null=True, upload_to='company_pdfs/')),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('job_type', models.CharField(choices=[('full-time', 'Full-time'), ('part-time', 'Part-time'), ('internship', 'Internship'), ('contract', 'Contract')], default='full-time', max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos/')),
                ('application_deadline', models.DateField(blank=True, null=True)),
                ('website_url', models.URLField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'company_profiles',
            },
        ),
    ]
