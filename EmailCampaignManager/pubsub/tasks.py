from celery import shared_task
from django.utils import timezone
from campaigns.models import Campaign
from .publisher import publish_email_campaign


# getting campaigns sheduled for today and publishing it to redis channel
@shared_task
def publish_daily_campaigns():
    print("publising started!")
    today = timezone.now().date()
    campaigns = Campaign.objects.filter(published_date__date=today)
    # print(campaigns)

    for campaign in campaigns:
        publish_email_campaign(campaign.id)

    print("publishing done")
