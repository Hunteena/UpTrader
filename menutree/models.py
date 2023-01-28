from django.core.exceptions import ValidationError
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
                  'и определяет название меню. '
                  'При изменении родителя будет изменена '
                  'последовательность предков для всех потомков.',
    )
    url = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Абсолютный или named URL',
        help_text='Введите URL для пункта меню. '
                  'Для меню (верхнеуровнего объекта без родителя) не нужен',
    )
    path = models.CharField(
        max_length=256,
        verbose_name='Последовательность предков',
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name

    def clean(self):
        if (self.id and self.parent
                and self.id in list(map(int, self.parent.path.split()))):
            raise ValidationError(
                f"Пункт меню '{self.parent}' нельзя использовать "
                f"в качестве родителя, потому что является потомком"
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.parent:
            self.path = f"{self.parent.path} {self.id}"
        else:
            self.path = f"{self.id} "
        super().save(*args, **kwargs, update_fields=['path'])
        if self.children:
            children = Item.objects.filter(parent_id=self.id)
            for child in children:
                child.save(*args, **kwargs)
