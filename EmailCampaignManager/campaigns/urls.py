from django.urls import path

from . import views

app_name = "campaigns"
urlpatterns = [
    path("", views.index, name="index"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("add_subscriber/", views.add_subscriber, name="add_subscriber"),
    path("trigger_campaign/<int:campaign_id>/", views.trigger_campaign, name="trigger_campaign"),
    path("render_campaign/<int:campaign_id>/", views.render_campaign_email, name="render_campaign_mail"),
    path("unsubscribe/<int:subscriber_id>/", views.unsubscribe, name='unsubscribe'),
]
