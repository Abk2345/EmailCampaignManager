from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from .models import Campaign, Subscriber
from django.utils.safestring import mark_safe

# send everyday at time -> 9:56 utc, using celery redis beat scheduling
@shared_task
def send_daily_campaigns():
    # Get today's date
    today = datetime.now().date()
    print("daily campaign sending function called")
    # Retrieve all campaigns scheduled for today
    campaigns = Campaign.objects.filter(published_date__date=today)
    subscribers = Subscriber.objects.filter(is_active=True)

    for campaign in campaigns:
        # Render the email content using the campaign information
        email_html = render_to_string('campaigns/email_template.html', {
            'subject': campaign.subject,
            'preview_text': campaign.preview_text,
            'article_url': campaign.article_url,
            'html_content': campaign.html_content,
        })

        # convert to safe html format
        email_html = mark_safe(email_html)

        # Create an EmailMultiAlternatives object for sending HTML emails
        email = EmailMultiAlternatives(
            subject=campaign.subject,
            body=campaign.plain_text_content,
            from_email="abhishant11@gmail.com",  # Replace with your email
            to=[subscriber.email for subscriber in subscribers],
        )

        # Attach the HTML content to the email
        email.attach_alternative(email_html, "text/html")

        # Send the email
        email.send()

    print("Send Email Daily Function Done!")

# send campaign email using url, using shared task of celery for optimization
@shared_task
def send_campaign_email(subject, preview_text, article_url, html_content, plain_text_content, subscribers):
    for subscriber in subscribers:
        # harcoded for now, since localhost
        unsubscribe_url = f"http://127.0.0.1:8000/app/unsubscribe/{subscriber['id']}/"
        html_content = mark_safe(html_content)

        email = EmailMultiAlternatives(
            subject,
            preview_text,
            "abhishant11@gmail.com",
            [subscriber['email']],
        )

        email_html = render_to_string('campaigns/email_template.html', {
            'subject': subject,
            'preview_text': preview_text,
            'article_url': article_url,
            'html_content': html_content,
            'unsubscribe_url': unsubscribe_url,
        })

        email.attach_alternative(email_html, "text/html")
        email.send()

