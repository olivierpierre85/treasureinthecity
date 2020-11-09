from django.contrib import admin

from .models import Puzzle, City, Place, PlacePuzzle, PuzzleCity, LogEvent

admin.site.register(Puzzle)
admin.site.register(City)
admin.site.register(Place)
admin.site.register(PlacePuzzle)
admin.site.register(PuzzleCity)
admin.site.register(LogEvent)