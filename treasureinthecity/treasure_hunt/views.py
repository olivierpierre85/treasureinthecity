import re
import json
import os
from django.conf import settings
from datetime import datetime, timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.core.mail import send_mail
from .models import Puzzle, Place, PlacePuzzle, City, PuzzleCity, LogEvent

def error(request):
    #TODO Specific wrong storeid ????

    create_log('error', 'Wrong place parameter', None, None)

    stored_id = ""
    if stored_id != "" :
        return render(request,'treasure_hunt/error.html')
    else:
        return render(request, 'treasure_hunt/error.html')

def home(request, place_id):
    try:
        place = Place.objects.get(pk=place_id)
        city = City.objects.get(pk=place.city.id)

        current_lang = get_language()
        if current_lang == 'fr' and city.name == 'Brussels' :
            # TODO replace by more durable solution
            city_name = 'Bruxelles'
            country_name = 'Belgique'
        else :
            city_name = city.name
            country_name = city.country


        # Select all puzzles for place
        place_puzzles = PlacePuzzle.objects.filter(place=place).order_by('order')
        # Get latest good answer for the place FOR THE USER
        latest_answer = current_puzzle = request.session.get('puzzle_order', 0) + 1
        visible_puzzles = place_puzzles[:latest_answer]

        create_log('first_page', '', place, None)

        main_subtitle = _('A Treasure Hunt Inside your Airbnb')
        page_title = _('Welcome')
        introduction = [_('So, I guess you\'re wondering what\'s all this about ?')]
        introduction.append(_('Well,') + '<strong>Treasure in the City</strong>' + _(' is an experience that will teach you a little about ') + '<strong>' + city_name + '</strong>' + _(' and ') + '<strong>'+ country_name + '</strong>' + _(' through ') + '<strong>' + str(place.number_of_puzzles()) + _(' different puzzles</strong>. Solve them with clues hidden in this apartment !'))
        introduction.append(_('Once you reach the last puzzle, you\'ll be able to guess the code of the treasure chest.'))
        introduction.append(_('Each Puzzle has <strong>hints</strong> to help you, but it\'s more fun if you don\'t use them !'))

        question_title = _('Enjoy!')

        return render(
            request,
            'treasure_hunt/home.html',
            {
                'place_id': place.name,
                'city' : city.name,
                'first_puzzle': place.first_puzzle,
                'visible_puzzles': visible_puzzles,
                'place_id' : place.id,
                'page_title' : page_title,
                'main_title': city.name,
                'main_subtitle': main_subtitle,
                'intro_title' : page_title,
                'introduction' : introduction,
                'question_title' : question_title,
            }
        )
    except :
        #TODO difference between uuid and other exception
        create_log('error', 'first page', None, None)
        return render(request,'treasure_hunt/error.html')


def puzzle(request, puzzle_id):
    try:
        place_puzzle = PlacePuzzle.objects.get(pk=puzzle_id)
        puzzle = Puzzle.objects.get(pk=place_puzzle.puzzle.id)
        place = Place.objects.get(pk=place_puzzle.place.id)
        puzzle_city = PuzzleCity.objects.filter(puzzle=place_puzzle.puzzle.id, city=place.city.id)[0]

        current_lang = get_language()

        # Set current order in session
        current_puzzle = request.session.get('puzzle_order', 0)
        if place_puzzle.order > current_puzzle:
            request.session['puzzle_order'] = place_puzzle.order

        # Select all puzzles for this place
        place_puzzles = PlacePuzzle.objects.filter(place=place).order_by('order')
        # Get latest good answer for the place FOR THE USER
        latest_answer = current_puzzle = request.session.get('puzzle_order', 0) + 1
        visible_puzzles = place_puzzles[:latest_answer]

        # WHEN READY EMAIL (TIMOUT for the moment, should try async send : https://stackoverflow.com/questions/32979945/django-send-mail-function-taking-several-minutes )
        # If last puzzle (solution), send mail (but not if already sent not long ago, to avoid spamming ) 
        # if place_puzzle.order == place.number_of_puzzles() :
        #     last_log = LogEvent.objects.filter(puzzle=place_puzzle.puzzle.id, place=place.id,type='open_puzzle').last()           
        #     allowed_seconds_diff = 5400 # 90 minutes
        #     if last_log == None or (datetime.now(timezone.utc) - last_log.created).seconds > allowed_seconds_diff :
        #         create_log('send_mail', '', place, puzzle)
        #         send_mail(
        #             _('Someone Found Your Treasure !'),
        #             _('Your current guest just opened the solution page of the puzzle.'),
        #             'info@unlockbrussels.be',
        #             [ place.email ],
        #             fail_silently=False,
        #         )
        if place_puzzle.order == place.number_of_puzzles() :
            create_log('open_solution', '', place, puzzle)
        else :
            create_log('open_puzzle', '', place, puzzle)


        # Get page content
        # #TODO url in prod ??? delete if not url = os.path.join(settings.STATIC_ROOT, 'treasureinthecity/treasure_hunt/content/' + place.city.name.lower() + '/' + puzzle.type + '.' + current_lang + '.json')
        url_static = os.path.join(settings.BASE_DIR, 'treasureinthecity/treasure_hunt'+ '/static/' + 'treasure_hunt/content/' + place.city.name.lower() + '/' + puzzle.type + '.' + current_lang + '.json')
        json_data = open(url_static)   
        content = json.load(json_data)
        json_data.close()

        main_subtitle = _('A Treasure Hunt Inside your Airbnb')

        return render(
            request,
            'treasure_hunt/' + puzzle.layout,
            {
                'city': place.city.name,
                'country':place.city.country,
                'next_puzzle': place_puzzle.next_puzzle,
                'first_puzzle': place.first_puzzle,
                'visible_puzzles': visible_puzzles,
                'place_id' : place.id,
                'puzzle_city': puzzle_city, # ???? DELETE TODO
                'page_title' : content['page_title'],
                'main_title': place.city.name,
                'main_subtitle': main_subtitle,
                'intro_title': content['intro_title'],
                'intro_subtitle': content['intro_subtitle'],
                'question_title': content['question_title'],
                'content' : content,
                'api_key': settings.GOOGLE_MAPS_API_KEY,
            }
        )
    except Exception as e:
        #TODO difference between uuid and other exception
        create_log('error', e, None, None)
        # return HttpResponse(e) # for debug purposes
        return render(request,'treasure_hunt/error.html')

def answer(request, puzzle_city_id, place_id):
    puzzle_city = PuzzleCity.objects.get(pk=puzzle_city_id)
    place = Place.objects.get(pk=place_id)
    answer = request.POST['answer_input']
    # fix for tinttin québec, TODO find more permanent solution
    if(answer.lower().replace('é', 'e') == puzzle_city.answer.lower()):
        result = 'true'
    else:
        result = 'false'
    
    create_log('answer ' + result , answer,place,puzzle_city.puzzle )

    return HttpResponse(result)

def log_event(request):
    # Save javascript event
    place = Place.objects.get(pk=request.POST['place'])
    puzzle = Puzzle.objects.get(pk=request.POST['puzzle'])
    create_log(request.POST['type'], request.POST['info'],place,puzzle )

    return HttpResponse()

def create_log(event_type, info, place, puzzle):
    log = LogEvent()
    log.type = event_type
    log.info = info
    log.place = place
    log.puzzle = puzzle

    log.save()
    return