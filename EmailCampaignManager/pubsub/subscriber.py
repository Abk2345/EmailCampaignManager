import redis
import threading
from django.conf import settings
from campaigns.views import trigger_send_campaign

def process_email_campaign(campaign_id):
    # campaign = Campaign.objects.get(id=campaign_id)
    print("process started")
    trigger_send_campaign(campaign_id)
    print("process ended")
    #  have to see whether it will work

def subscribe_to_email_campaigns():
    print("subscribe started")
    r = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
   #SUBSCRIBE TO CHANNEL
    pubsub = r.pubsub()
    pubsub.subscribe('email_campaigns')

    for item in pubsub.listen():
        if item['type'] == 'message':
            campaign_id = int(item['data'])
            thread = threading.Thread(target=process_email_campaign, args=(campaign_id,))
            thread.start()

    print("subscribe ended!")




