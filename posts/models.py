from django.conf import settings
from django.db import models
from utils.mixins import TimeStampsMixin

class Post(TimeStampsMixin, models.Model):
    slug = models.SlugField(max_length=40, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    text = models.TextField()
    approved = models.BooleanField(default=True)

    def add_comment(self, author, text):
        return Comment.objects.create(post=self, author=author, text=text)

    def get_comments(self):
        return self.post_comments.filter(parent__isnull=True).order_by('date_created')

    @property
    def comments(self):
        return self.get_comments()

    class Meta:
        permissions = (
            ('share_post', 'Share Post'),
            ('comment_on_post', 'Comment on Post'),
        )

class Comment(TimeStampsMixin, models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    post = models.ForeignKey('Post', related_name='post_comments')
    parent = models.ForeignKey('self', related_name='comment_children', null=True, blank=True)

    def add_comment(self, author, text):
        return Comment.objects.create(post=self.post, parent=self, author=author, text=text)

    def get_comments(self):
        return self.comment_children.all().order_by('date_created')

    @property
    def comments(self):
        return self.get_comments()
