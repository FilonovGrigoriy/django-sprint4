from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
        help_text='Дата и время добавления.',
    )

    class Meta:
        abstract = True


class Category(CreatedAtModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
        help_text='Максимальная длина — 256 символов.',
    )
    description = models.TextField(
        'Описание',
        help_text='Опишите, для каких публикаций эта категория.',
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(CreatedAtModel):
    name = models.CharField(
        'Название места',
        max_length=256,
        help_text='Максимальная длина — 256 символов.',
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        # В дампе/миграциях Практикума ожидается именно такой help_text.
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(CreatedAtModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
        help_text='Максимальная длина — 256 символов.',
    )
    text = models.TextField(
        'Текст',
        help_text='Основной текст публикации.',
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        default=timezone.now,
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации',
        help_text='Автор, создавший эту публикацию.',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория',
        help_text='Категория, к которой относится публикация.',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение',
        help_text=(
            'Место, к которому относится публикация '
            '(можно не указывать).'
        ),
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Comment(CreatedAtModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField('Текст')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return f'Комментарий {self.pk} к посту {self.post_id}'
