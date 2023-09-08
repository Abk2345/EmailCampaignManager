from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Subscriber, Campaign
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.core.mail import send_mail
from .tasks import send_campaign_email
from datetime import datetime
import time
from django.shortcuts import render

def index(request):
    return HttpResponse("This is index page of email campaign django app.")



# done
def fetch_data(campaign_id):
    campaign = Campaign.objects.get(pk=campaign_id)
    subject = campaign.subject
    preview_text = campaign.preview_text
    article_url = campaign.article_url
    html_content = campaign.html_content
    plain_text_content = campaign.plain_text_content

    subscribers = Subscriber.objects.filter(is_active=True)
    subscriber_data = [
        {
            'id': subscriber.id,
            'email': subscriber.email,
            'first_name': subscriber.first_name,
        }
        for subscriber in subscribers
    ]
    return subject, preview_text, article_url, html_content, plain_text_content, subscriber_data

# done
def render_campaign_email(request, campaign_id):
    subject, preview_text, article_url, html_content, plain_text_content, subscribers = fetch_data(campaign_id)

    html_content = mark_safe(html_content)
    email_html = render_to_string('campaigns/email_template.html', {
        'subject': subject,
        'preview_text': preview_text,
        'article_url': article_url,
        'html_content': html_content,
    })
    return HttpResponse(email_html)


def trigger_send_campaign(campaign_id):
    subject, preview_text, article_url, html_content, plain_text_content, subscribers = fetch_data(campaign_id)
    print("Entry to trigger campaign!")
    # simple looping and sending emails using mailgun
    # start_time = time.time()
    #
    # for subscriber in subscribers:
    #     # Harcoded for now, since localhost
    #     unsubscribe_url = f"http://127.0.0.1:8000/app/unsubscribe/{subscriber['id']}/"
    #     html_content = mark_safe(html_content)
    #
    #     email = EmailMultiAlternatives(
    #         subject,
    #         preview_text,
    #         "abhishant11@gmail.com",
    #         [subscriber['email']],
    #     )
    #
    #     email_html = render_to_string('campaigns/email_template.html', {
    #         'subject': subject,
    #         'preview_text': preview_text,
    #         'article_url': article_url,
    #         'html_content': html_content,
    #         'unsubscribe_url': unsubscribe_url,
    #     })
    #
    #     email.attach_alternative(email_html, "text/html")
    #     email.send()
    #
    # end_time = time.time()
    # execution_time = end_time - start_time
    #
    # print(f"Simple Loop: Time taken to send emails: {execution_time} seconds")

    # using celery parallelisation technique
    start_time = time.time()
    send_campaign_email.delay(
        subject,
        preview_text,
        article_url,
        html_content,
        plain_text_content,
        subscribers,
    )
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Celery: Time taken to schedule email task: {execution_time} seconds")
    print("Exit from trigger campaign!")
    return HttpResponse("Email sending task scheduled successfully!")


# done ->  Optimization
# Simple Loop: Time taken to send emails: 20.203108072280884 seconds for 3 verified reciepients email ids
# Celery: Time taken to schedule email task: 0.07072186470031738 seconds
def trigger_campaign(request, campaign_id):
    subject, preview_text, article_url, html_content, plain_text_content, subscribers = fetch_data(campaign_id)

    # simple looping and sending emails using mailgun
    # start_time = time.time()
    #
    # for subscriber in subscribers:
    #     # Harcoded for now, since localhost
    #     unsubscribe_url = f"http://127.0.0.1:8000/app/unsubscribe/{subscriber['id']}/"
    #     html_content = mark_safe(html_content)
    #
    #     email = EmailMultiAlternatives(
    #         subject,
    #         preview_text,
    #         "abhishant11@gmail.com",
    #         [subscriber['email']],
    #     )
    #
    #     email_html = render_to_string('campaigns/email_template.html', {
    #         'subject': subject,
    #         'preview_text': preview_text,
    #         'article_url': article_url,
    #         'html_content': html_content,
    #         'unsubscribe_url': unsubscribe_url,
    #     })
    #
    #     email.attach_alternative(email_html, "text/html")
    #     email.send()
    #
    # end_time = time.time()
    # execution_time = end_time - start_time
    #
    # print(f"Simple Loop: Time taken to send emails: {execution_time} seconds")

    # using celery parallelisation technique
    start_time = time.time()
    send_campaign_email.delay(
        subject,
        preview_text,
        article_url,
        html_content,
        plain_text_content,
        subscribers,
    )
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Celery: Time taken to schedule email task: {execution_time} seconds")
    return HttpResponse("Email sending task scheduled successfully!")

# done
def subscribe(request):
    return render(request, 'campaigns/subscribe.html')
# done
def add_subscriber(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')

        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            subscriber.first_name = first_name
            subscriber.save()

            return HttpResponse("Subscriber added successfully!")
        else:
            return render(request, 'campaigns/subscribe.html', {'error_message': 'Email is required'})

    return render(request, 'campaigns/subscribe.html')

#done
def unsubscribe(request, subscriber_id):
    try:
        subscriber = Subscriber.objects.get(pk=subscriber_id)
        subscriber.is_active = False
        subscriber.save()
        return HttpResponse("You have unsubscribed successfully!")
    except Subscriber.DoesNotExist:
        return HttpResponse("Subscriber not found.", status=404)
