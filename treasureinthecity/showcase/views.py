import json
import os
from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template, select_template
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.core.mail import send_mail
from django.http import HttpResponse

def index(request):
    #generic home page
    return render(request,'showcase/index.html')

def city(request, city):
    # Get city template, or error page
    # template = select_template(['showcase/' + city +  '.html','treasure_hunt/error.html'])
    template = select_template(['showcase/main_layout.html','treasure_hunt/error.html'])

    # Get content for city based on language
    current_lang = get_language()
    
    url_static = os.path.join(settings.BASE_DIR, 'treasureinthecity/showcase'+ '/static/' + 'showcase/content/' + city.lower() + '.' + current_lang + '.json')
    json_data = open(url_static)   #TODO url in prod 
    content = json.load(json_data)
    json_data.close()

    return render(request, template.template.name, {'content' : content, 'city' : city.lower()})

def email(request):
    #TODO send email for more info
    email_body = ( 
        'You have received a new message from your website contact form.\n\n'
        'Name: ' + request.POST.get('name', 'empty') + '\n' 
        'Email: ' + request.POST.get('email', 'empty') + '\n'
        'Phone: ' + request.POST.get('phone', 'empty') + '\n'
        'Message:\n' + request.POST.get('message', 'empty')
    )

    send_mail(
        'Contact for Treasure in the city !',
        email_body ,
        'info@treasureinthecity.com	',
        ['olivierpierre85@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse()