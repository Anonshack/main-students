import random
import string
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save


class Article(models.Model):
    title = models.CharField(max_length=221, db_index=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='articles', null=True, blank=True, help_text='2MB is limit')
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.id})"

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     try:
    #         super().save()
    #     except Exception as e:
    #         rand = "".join(random.choice(string.ascii_lowercase) for i in range(4))
    #         self.slug = slugify(self.title) + f"-{rand}"
    #         super().save()


# def article_pre_save(sender, instance, *args, **kwargs):
#     if instance.slug is None:
#         instance.slug = slugify(instance.title)


def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        if instance.slug is None:
            instance.slug = slugify(instance.title)
            try:
                instance.save()
            except Exception as e:
                rand = "".join(random.choice(string.ascii_lowercase) for _ in range(4))
                instance.slug = slugify(instance.title) + f"-{rand}"
                instance.save()


# pre_save.connect(article_pre_save, sender=Article)
post_save.connect(article_post_save, sender=Article)