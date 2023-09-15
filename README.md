# EmailCampaignManager

This repository contains code for Managing email-campaign web application using django

Various Endpoints for different purposes

Documentation link: https://docs.google.com/document/d/16AwiQdgFTBiJHU1EyL4BXkA3EcCIeHFrnTfyOAO_gSY/edit?usp=sharing

# Steps to Install
1. Clone the application, create and run the python virtual environment
2. Configure your mailgun account, add verified reciepients for free account credentials in settings.py
3. Install requirements.txt in your directory
4. Run app
    1. For Api's endpoints in documentation: run command: python manage.py runserver in your terminal
    2. Add some data through admin site, to both Subscriber as well as Campaign database Tables
    3. For trigger_campaign api endpoint which uses celery to optimize sending of mails -> 
         1. run redis-server on your device after installing it, and on another terminal
         2. run command: celery -A project_name workers --loglevel=info, then test this api
    4. For multi-threading pub-sub optimization using celery beat, run another terminal for beat scheduling, set scheduling
         1. time in settings.py then
         2. run command: celery -A project_name beat --loglevel=info, then test this functionality


# Hope you Enjoyed The Project!
