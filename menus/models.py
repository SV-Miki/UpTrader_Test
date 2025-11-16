from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name="items", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )

    url = models.CharField(max_length=500, blank=True)
    named_url = models.CharField(max_length=200, blank=True)

    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Menu item"
        verbose_name_plural = "Menu items"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.menu.name}: {self.title}"

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except Exception:
                return self.named_url
        return self.url or ""
