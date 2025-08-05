from django.db import models


class Breed(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название породы",
        help_text="Введите название породы",
    )
    description = models.TextField(
        verbose_name="Описание породы",
        help_text="Введите описание породы",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"

    def __str__(self):
        return self.name


class Dog(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Кличка", help_text="Введите кличку собаки"
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        verbose_name="Порода",
        help_text="Введите породу собаки",
        null=True,
        blank=True,
        related_name="dogs",
    )
    photo = models.ImageField(
        upload_to="dogs/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото собаки",
    )
    date_born = models.DateField(blank=True, null=True, verbose_name="", help_text="")

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"
        ordering = ["breed", "name"]

    def __str__(self):
        return self.name
