# Generated by Django 3.2.13 on 2022-07-07 12:49

import django.db.models.deletion
import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('type', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('maturity_state', models.CharField(max_length=15)),
                ('modification_date', models.DateTimeField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(blank=True, null=True)),
                ('responsible', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ebom0000',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(blank=True, max_length=3, null=True)),
                ('title', models.CharField(max_length=50)),
                ('revision', models.CharField(max_length=2)),
                ('state', models.CharField(max_length=15)),
                ('critical', models.CharField(blank=True, max_length=15, null=True)),
                ('seriality', models.CharField(blank=True, max_length=15, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='posts/', verbose_name='upload file')),
                ('import_selection', models.CharField(choices=[('E', 'EBOM'), ('M', 'MBOM'), ('R', 'ROUT'), ('I', 'ITEM')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=25)),
                ('bom_ver', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (70, 70), (71, 71), (72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (79, 79), (80, 80), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (90, 90), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99)])),
                ('rout_ver', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (70, 70), (71, 71), (72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (79, 79), (80, 80), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (90, 90), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99)])),
            ],
        ),
        migrations.CreateModel(
            name='Projectlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField()),
                ('time_spent', models.DecimalField(decimal_places=2, default=models.DecimalField(decimal_places=2, max_digits=5), max_digits=5)),
                ('time_left', models.DecimalField(decimal_places=2, default=models.DecimalField(decimal_places=2, max_digits=5), max_digits=5)),
                ('person', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prototype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msn', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Shopeflore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sta', models.CharField(max_length=25)),
                ('sta_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_status_description', models.CharField(max_length=10)),
                ('task_status', models.CharField(choices=[('W', 'READY TO WORK'), ('W', 'IN WORK'), ('V', 'READY FOR CHECK'), ('H', 'ON HOLD'), ('T', 'IN CHECK'), ('R', 'RELEASED'), ('C', 'CHECKED'), ('N', 'CANCELED')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Tow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tow_name', models.CharField(max_length=3)),
                ('tow_desc', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_root', models.CharField(max_length=10)),
                ('siq', models.CharField(max_length=3)),
                ('text', models.TextField(help_text='Input test', verbose_name='Note')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Completed Date')),
                ('completed_date', models.DateField(verbose_name='Due Date')),
                ('time_consume', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='posts.action')),
                ('bom0000', models.ManyToManyField(blank=True, null=True, to='posts.Ebom0000')),
                ('item', models.ForeignKey(blank=True, max_length=25, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ttask', to='posts.item')),
                ('msn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='posts.prototype')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks_project', to='posts.projectlist')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='posts.status')),
                ('tow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskstow', to='posts.tow')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=25)),
                ('text', models.TextField(blank=True, help_text='Input test', verbose_name='Note')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('completed_date', models.DateField()),
                ('siq', models.CharField(max_length=3)),
                ('tow', models.CharField(blank=True, max_length=3, null=True)),
                ('time_consume', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttask', to='posts.action')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttask', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttask', to='posts.status')),
                ('task_s', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttask', to='posts.tasks')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ReportMsn0000',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='posts.item')),
                ('msn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='posts.prototype')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='posts.shopeflore')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст поста', verbose_name='Текст поста')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Картинка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('group', models.ForeignKey(blank=True, help_text='Группа, к которой будет относиться пост', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post', to='posts.group', verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='msn',
            field=models.ManyToManyField(blank=True, null=True, related_name='items_msn', through='posts.ReportMsn0000', to='posts.Prototype'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст комментария', verbose_name='Текст комментария')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post', verbose_name='комментарий')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='user_author'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(('author', django.db.models.expressions.F('user')), _negated=True), name='author_not_user'),
        ),
    ]
