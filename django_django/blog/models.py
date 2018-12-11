from django.db import models
import datetime
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(u'Заголовок', max_length=255)
    text = models.TextField(u'Текст')
    date = models.DateTimeField(u'Дата создания', default=now, blank=True)
    hidden = models.BooleanField(u'Скрытый пост', default=False)

    def __str__(self):
        return f'Post: {self.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(u'Текст')
    date = models.DateTimeField(u'Дата создания', default=now, blank=True)
    reply_to = models.ForeignKey('blog.Comment', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'Commend: {self.text}'
