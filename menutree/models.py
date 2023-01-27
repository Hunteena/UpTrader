from django.db import models


class Item(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='Родитель',
        help_text='Если родитель не задан, то объект является верхнеуровневым '
                  'и определяет название меню',
    )
    url = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Путь (после домена)',
        help_text='Введите путь в формате /somepath/. '
                  'Для меню (верхнеуровнего объекта без родителя) не нужен',
    )
    path = models.CharField(
        max_length=256,
        verbose_name='Последовательность предков',
    )

    class Meta:
        ordering = ['path']
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.parent:
            self.path = f"{self.parent.path} {self.id}"
        else:
            self.path = f"{self.id} "
        super().save(*args, **kwargs, update_fields=['path'])
        # TODO change children's path on updating parent
