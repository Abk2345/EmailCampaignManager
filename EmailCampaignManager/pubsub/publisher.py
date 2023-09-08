import redis
from django.conf import settings

# for publishing campaign id on redis channel
def publish_email_campaign(campaign_id):
    r = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
    r.publish('email_campaigns', campaign_id)
    print("publishing done!")
