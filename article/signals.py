from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.dispatch import receiver
import random, string

from .models import Article


@receiver(pre_save, sender=Article)
def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)
        try:
            instance.save()
        except Exception as e:
            rand = "".join(random.choice(string.ascii_lowercase) for _ in range(4))
            instance.slug = slugify(instance.title) + f"-{rand}"
            instance.save()


pre_save.connect(article_pre_save, sender=Article)