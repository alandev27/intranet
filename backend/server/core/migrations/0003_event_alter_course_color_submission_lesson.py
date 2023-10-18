# Generated by Django 4.2.6 on 2023-10-18 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_parent_options_alter_student_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('color', models.CharField(blank=True, max_length=7, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='color',
            field=models.CharField(choices=[('R', 'Red'), ('B', 'Blue'), ('G', 'Green'), ('Y', 'Yellow'), ('O', 'Orange'), ('P', 'Purple'), ('W', 'White')], default='W', max_length=7),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(blank=True, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('submitted', models.BooleanField(default=False)),
                ('submittedAt', models.DateTimeField(blank=True, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assignment')),
                ('attachments', models.ManyToManyField(blank=True, to='core.attachment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.event')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
            ],
            bases=('core.event',),
        ),
    ]