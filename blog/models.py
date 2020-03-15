from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe

fs = FileSystemStorage(location='blog/media/photos')


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    # photo = models.ImageField(storage=fs, upload_to='blog/media/photos')
    photo = models.ImageField(upload_to='article')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __iter__(self):
        field_names = [f.name for f in self._meta.fields]
        for field_name in field_names:
            value = getattr(self, field_name, None)
            yield (field_name, value)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='', blank=True)
    biography = models.TextField(default='', blank=True)

    def __str__(self):
        return self.user.username

    # Здесь я возвращаю аватарку или картинку , если аватар не выбран
    def get_avatar(self):
        if not self.avatar:
            return '/static/img/default_avatar.png'
        return self.avatar.url

    # метод, для создания фейкового поля таблицы в режиме read only
    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())

    avatar_tag.short_description = 'Avatar thumb'


def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()


post_save.connect(create_user_profile, sender=User)
