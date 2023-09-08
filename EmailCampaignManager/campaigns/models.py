from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# for using celery pub-sub architecture for parallel execution
from django.db.models.signals import post_save
from django.dispatch import receiver
from pubsub.publisher import publish_email_campaign

# database model schema for Subscribers
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

# database model schema for Campaign
class Campaign(models.Model):
    subject = models.CharField(max_length=200)
    preview_text = models.TextField()
    article_url = models.URLField()
    html_content = models.TextField()
    plain_text_content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
