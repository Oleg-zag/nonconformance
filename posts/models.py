from inspect import signature

from django.contrib.auth import get_user_model
from django.db import models

from posts.constant import (CM, DE, DO, DOEPSEWIS, DOFS, DOMP, DOPWD, DOSTR,
                            DOSTRS, HEAD, LEAD, ME, MELEAD, MEMNG, MEPLANER,
                            OAW, PE, PM, PME, SE, SUPER, TE, VTXPOME, VTXPOMG,
                            VTXPOMP, VTXPOQA, VTXPOSC, VTXPOSF)

User = get_user_model()

LEN_OF_TEXT = 15


class Company(models.Model):
    name = models.CharField(max_length=50)
    shot_name = models.CharField(max_length=3)
    country = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    adress = models.TextField()

    def __str__(self):
        return self.name


class Group(models.Model):
    GENERAL = "GENERAL"
    MEELCTR = "ME ELECTRICAL"
    MESTRCT = "ME STRUCTURAL"
    MEEQPMT = "ME EQUPMENT"
    MEFTEST = "ME FUNCTIONAL TEST"
    GROUP_SELECTION = [
        (GENERAL, 'GNRL'),
        (MEELCTR, 'MELC'),
        (MESTRCT, 'MSTR'),
        (MEEQPMT, 'MEQP'),
        (MEFTEST, 'MFTS'),
    ]
    group = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=GROUP_SELECTION,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.group


class Profile(models.Model):
    DEPARTMENT_OF_CHOISES = [
        (VTXPOME, 'VTX MANUFACTURING ENGINEERING'),
        (VTXPOSC, 'VTX SUPPLY CHAIN'),
        (VTXPOSF, 'VTX SHOP FLOOR'),
        (VTXPOQA, 'VTX PRODUCTION QUALITY'),
        (VTXPOMP, 'VTX MATERIAL PLANING'),
        (VTXPOMG, 'VTX MANAGMENT GROUP'),
        (OAW, 'OAW'),
        (DOEPSEWIS, 'EPS&EWIS'),
        (DOFS, 'DOFS'),
        (SUPER, 'ADMIN'),
        (CM, 'CM'),
        (DO, 'DO'),
        (DOSTR, 'DOSTR'),
        (DOSTRS, 'DOSTRS'),
        (DOPWD, 'DOPWD'),
        (DOMP, 'DOM&P'),
    ]
    ROLE_OF_CHOISES = [
        (ME, 'ME'),
        (MEMNG, 'ME MANAGER'),
        (MEPLANER, 'ME PLANER'),
        (PM, 'PRODUCTION MANAGER'),
        (LEAD, 'LE'),
        (HEAD, 'HEAD'),
        (SUPER, 'ADMIN'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    department = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=DEPARTMENT_OF_CHOISES,
    )
    role = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=ROLE_OF_CHOISES,
    )
    image = models.ImageField(
        'Avatar',
        upload_to='posts/',
        blank=True,
        null=True,
    )
    signature = models.ImageField(
        'Signature',
        upload_to='posts/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.department

  #  @receiver(post_save, sender=User)
  #  def create_user_profile(sender, instance, created, **kwargs):
  #      if created:
  #        Profile.objects.create(user=instance)

   # @receiver(post_save, sender=User)
   # def save_user_profile(sender, instance, **kwargs):
   #     instance.profile.save()


class Post(models.Model):
    text = models.TextField(
        'Post Text',
        help_text='Input post text',
    )
    pub_date = models.DateField(
        'Publish date',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Author',
    )
    group = models.ForeignKey(
        Group,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='post',
        verbose_name='Group',
        help_text='Group?',
    )
    image = models.ImageField(
        'Picture',
        upload_to='posts/',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.text[:LEN_OF_TEXT]


class Comment(models.Model):
    text = models.TextField(
        'Comment text',
        help_text='Input comment text',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='comments',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    created = models.DateField(
        'Publish date',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created']


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='user_author'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name="author_not_user"
            ),
        ]


class Action(models.Model):
    name = models.CharField(max_length=15, unique=True)
    type = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    maturity_state = models.CharField(max_length=50)
    modification_date = models.DateTimeField(        
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    responsible = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Status(models.Model):
    READY_TO_WORK = 'W'
    INWORK = 'W'
    RFCHECK = 'V'
    ONHOLD = 'H'
    INCHECK = 'T'
    RELEASED = 'R'
    CHECKED = 'C'
    CANCELED = 'N'
    STATUS_OF_TASK_CHOISES = [
        (READY_TO_WORK, 'READY TO WORK'),
        (INWORK, 'IN WORK'),
        (RFCHECK, 'READY FOR CHECK'),
        (ONHOLD, 'ON HOLD'),
        (INCHECK, 'IN CHECK'),
        (RELEASED, 'RELEASED'),
        (CHECKED, 'CHECKED'),
        (CANCELED, 'CANCELED'),
    ]
    task_status_description = models.CharField(
        max_length=10,
    )
    task_status = models.CharField(
        max_length=1,
        choices=STATUS_OF_TASK_CHOISES,
    )

    def __str__(self):
        return self.task_status_description


class Prototype(models.Model):
    msn = models.CharField(max_length=7)

    def __str__(self):
        return self.msn


class Tow(models.Model):
    tow_name = models.CharField(
        max_length=3,
    )
    tow_desc = models.CharField(max_length=25)

    def __str__(self):
        return self.tow_name


class Shopeflore(models.Model):
    sta = models.CharField(max_length=25)
    sta_name = models.CharField(max_length=25)

    def __str__(self):
        return self.sta_name


class Import(models.Model):
    file = models.FileField(
        'upload file',
        upload_to='posts/',
        blank=True,
        null=True,
    )
    EBOM = 'E'
    MBOM = 'M'
    ROUT = 'R'
    ITEM = 'I'
    STATUS_OF_CHOISES = [
        (EBOM, 'EBOM'),
        (MBOM, 'MBOM'),
        (ROUT, 'ROUT'),
        (ITEM, 'ITEM'),
    ]
    import_selection = models.CharField(
        max_length=1,
        choices=STATUS_OF_CHOISES,
    )


class Ebom0000(models.Model):

    title = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    revision = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    state = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Item(models.Model):
    VER=[(i, i) for i in range (100)]
    name = models.CharField(
        max_length=100,
        unique=True,
        )
    description = models.CharField(
        max_length=100,
        null=True,
    )
    msn = models.ManyToManyField(
        Prototype, through='ReportMsn0000',
        blank=True,
        null=True,
        related_name='items_msn',
    )
    bom = models.ManyToManyField(
        Ebom0000,
        null=True,
        blank=True,
    )
    bom_ver = models.IntegerField(
        blank=True,
        null=True,
        choices=VER,
    )
    rout_ver = models.IntegerField(
        blank=True,
        null=True,
        choices=VER,
    )
    def __str__(self):
        return self.name


class Projectlist(models.Model):
    name = models.CharField(max_length=20)
    time = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    person = models.ManyToManyField(
        User,
        blank=True,
        null=True,
    )
    description = models.TextField()
    time_spent = models.DecimalField(
        default=time,
        max_digits=5,
        decimal_places=2,
    )
    time_left = models.DecimalField(
        default=time,
        max_digits=5,
        decimal_places=2,
    )

    def __str__(self):
        return self.name


class Tasks(models.Model):
    event_root = models.CharField(max_length=10)
    siq = models.CharField(max_length=20)
    item = models.ForeignKey(
        Item,
        null=True,
        max_length=25,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='ttask',
    )
    group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    planned_time = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    bom0000 = models.ManyToManyField(
        Ebom0000,
        null=True,
        blank=True,
    )
    text = models.TextField(
        'Note',
        help_text='Input test',
    )
    date = models.DateField(
        'Date',
        auto_now_add=True,
    )
    completed_date = models.DateField(
        'Due Date',
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='tasks')
    person = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    action = models.ForeignKey(
        Action,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    msn = models.ForeignKey(
        Prototype,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    tow = models.ForeignKey(
        Tow,
        on_delete=models.CASCADE,
        related_name='taskstow',
    )
    project = models.ForeignKey(
        Projectlist,
        on_delete=models.CASCADE,
        related_name='tasks_project',
    )
    time_consume = models.DecimalField(
        blank=True,
        null=True,
        default=0,
        max_digits=5,
        decimal_places=2)
    #image = models.FileField(
    #    'Picture',
    #    upload_to='posts/',
    #    blank=True,
    #    null=True,
    #)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.item


class Task(models.Model):
    task_name = models.CharField(max_length=25)
    text = models.TextField(
        'Note',
        blank=True,
        help_text='Input test',
    )
    date = models.DateField(
        'Date',
        auto_now_add=True,
    )
    task_s = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name='ttask'
    )
    completed_date = models.DateField(
        'completed_date',
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='ttask')
    person = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ttask',
    )
    image = models.FileField(
        'Picture',
        upload_to='posts/',
        blank=True,
    )
    action = models.ForeignKey( 
        Action,
        on_delete=models.CASCADE,
        related_name='ttask',
    )
    siq = models.CharField(max_length=3)
    tow = models.CharField(
        max_length=3,
        blank=True,
        null=True,
    )
    time_consume = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        ordering = ['-date']


class ReportMsn0000(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='reports')
    msn = models.ForeignKey(
        Prototype,
        on_delete=models.CASCADE,
        related_name='reports')
    station = models.ForeignKey(
        Shopeflore,
        null=True,
        on_delete=models.CASCADE,
        related_name='reports',
    )

    def __str__(self):
        return self.item.name
