from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Имя группы', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание')

    class Meta:
        ordering = ['id']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.text[:15]} ...'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.text[:15]} ...'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_users')
        ]
