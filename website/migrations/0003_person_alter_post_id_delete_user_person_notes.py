# Generated by Django 4.0.2 on 2022-02-04 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_post_user_username_user_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='person',
            name='notes',
            field=models.ManyToManyField(blank=True, to='website.Post'),
        ),
    ]