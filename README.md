# EmailCampaignManager

This repository contains code for Managing email-campaign web application using django

Various Endpoints for different purposes

Documentation link: https://docs.google.com/document/d/16AwiQdgFTBiJHU1EyL4BXkA3EcCIeHFrnTfyOAO_gSY/edit?usp=sharing

# Steps to Install

Step 1: Clone the application, create and run the python virtual environment
Step 2: Configure your mailgun account, add verified reciepients for free account credentials in settings.py
Step 3: Install requirements.txt in your directory
Step 4: Run app
  -> For Api's endpoints in documentation: run command: python manage.py runserver in your terminal
  -> Add some data through admin site, to both Subscriber as well as Campaign database Tables
  -> For trigger_campaign api endpoint which uses celery to optimize sending of mails -> 
            run redis-server on your device after installing it, and on another terminal
            run command: celery -A project_name workers --loglevel=info, then test this api
  -> For multi-threading pub-sub optimization using celery beat, run another terminal for beat scheduling, set scheduling
            time in settings.py then
            run command: celery -A project_name beat --loglevel=info, then test this functionality


# Hope you Enjoyed The Project!
