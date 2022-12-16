from django.db import models

from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path


class AdvUser(AbstractUser):
    """Клас для перевизначення стандартної моделі користувача AbstractUser"""

    if_activated = models.BooleanField(default=True, db_index=True, verbose_name='Пройшов активацію?')
    send_massage = models.BooleanField(default=True, verbose_name='Відсилати сповіщення про нові комментарі?')

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)


    class Meta(AbstractUser.Meta):
        pass


class Rubric (models.Model):
    """Клас для визначення базової моделі рубрики"""
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Назва')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надрубрика')


class SuperRubricManager(models.Manager):
    """Клас для визначення надрубрик"""

    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    """Клас для визначення надрубрик"""

    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = "Надрубрика"
        verbose_name_plural = 'Надрубрика'


class SubRubricManager(models.Manager):
    """Клас для визначення підрубрик"""

    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    """Клас для визначення підрубрик"""

    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Підрубрика'
        verbose_name_plural = 'Підрубрика'


class Bb(models.Model):
    """"Клас для визначення моделі оголошень"""

    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубріка')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Опис')
    price = models.FloatField(default=0, verbose_name='Вартість')
    contacts = models.TextField(verbose_name='Контактна інформація')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Зображення')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор оголошення')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Виводити у перелік?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубліковано')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Оголошення'
        verbose_name = 'Оголошення'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    """Клас для додаткових ілюстрацій"""
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Оголошення')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Зображення')

    class Meta:
        verbose_name_plural = 'Додаткова ілюстрації'
        verbose_name = 'Додаткова ілюстрації'


class Comment(models.Model):
    """Клас для занесення коментарів"""
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Оголошення')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Зміст')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Виводити на екран')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубліковано')

    class Meta:
        verbose_name_plural = 'Коментарі'
        verbose_name = 'Коментарі'
        ordering = ['created_at']

