from django.db import models
from django.contrib.auth.models import User

from PIL import Image
from django.utils import timezone


class Profile(models.Model):

    GROUP = (
        ('CSc', 'Computer Science'),
        ('SE', 'Software engineering'),
        ('BDA', 'Big Data'),
        ('MT', 'Media Tech' ),
        ('IA', 'Industrial automation'),
        ('ITM', 'IT Management'),
        ('CS', 'Cyber security')
    )
    IS_USER = (
        ('student', 'student'),
        ('teacher', 'teacher'),
        ('club', 'club')
    )
    bio = models.CharField(max_length = 250,  blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    studentgroup = models.CharField(default='choose',max_length=3, choices=GROUP)
    is_user = models.CharField(default='teacher', max_length=7, choices=IS_USER)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
