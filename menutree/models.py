from django.db import models


class Menu(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название меню',
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=128,
                            verbose_name='Название пункта меню')
    url = models.CharField(max_length=256)
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Меню',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='Родительский пункт меню',
    )
    path = models.CharField(max_length=256)

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
            self.path = f"{self.menu_id} {self.id}"
        super().save(*args, **kwargs, update_fields=['path'])
        # TODO change children's path on updating parent
