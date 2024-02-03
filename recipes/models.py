from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
import random, string


class Tag(models.Model):
    title = models.CharField(max_length=221, unique=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=221, db_index=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    UNIT = (
        (0, 'GRAMM'),
        (1, 'MILLILITR'),
        (2, 'DONA'),
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    title = models.CharField(max_length=221)
    quantity = models.IntegerField()
    unit = models.IntegerField(choices=UNIT)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def recipe_post_save(sender, instance, created, *args, **kwargs):
    if created:
        if instance.slug is None:
            instance.slug = slugify(instance.title)
            try:
                instance.save()
            except Exception as e:
                rand = "".join(random.choice(string.ascii_lowercase) for _ in range(4))
                instance.slug = slugify(instance.title) + f"-{rand}"
                instance.save()


post_save.connect(recipe_post_save, sender=Recipe)