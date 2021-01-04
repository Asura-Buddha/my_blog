from django.conf import settings
from django.db import models
from django.utils import timezone


class AuthorBase(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TextBase(models.Model):
    text = models.TextField()

    class Meta:
        abstract = True


class CreatedDateBase(models.Model):
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Post(AuthorBase, TextBase, CreatedDateBase):
    title = models.CharField(max_length=200)
    published_date = models.DateTimeField(blank=True, null=True)
    cover = models.ImageField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()


class PostBase(models.Model):
    post = models.ForeignKey(Post, related_name='%(class)ss', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(AuthorBase, TextBase, CreatedDateBase, PostBase):

    def __str__(self):
        return str(self.author) + ": " + self.text


class Like(AuthorBase, PostBase):
    class Meta:
        unique_together = ['author', 'post']

    def __str__(self):
        return str(self.author) + ": " + str(self.post)
