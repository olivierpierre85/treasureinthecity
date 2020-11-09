import uuid 
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200, default="TODO Country")
    
    def __str__(self):
            return self.name

class Puzzle(models.Model):
    name = models.CharField(max_length=200, default="Puzzle")
    type = models.CharField(max_length=200)
    layout = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Place(models.Model):
    id = models.UUIDField(
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    email = models.CharField(max_length=200,default=None, null=True) # TODO MOVE TO Customer class when needed
    
    def __str__(self):
        return self.name

    def number_of_puzzles(self):
        nb_puzzles = PlacePuzzle.objects.filter(place=self.id).count() -1 #-1 because solution.html not counted
        return nb_puzzles
    
    def first_puzzle(self):
        return PlacePuzzle.objects.filter(place=self.id, order=0).first()  

class PlacePuzzle(models.Model):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.place.name + ' - ' + self.puzzle.name

    def next_puzzle(self):
        return PlacePuzzle.objects.filter(place=self.place, order=(self.order + 1)).first()  

class PuzzleCity(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    answer = models.TextField(default="answer")
    
    def __str__(self):
        return self.puzzle.name + ' - ' + self.city.name

class LogEvent(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE,default=None, null=True)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE,default=None, null=True)
    type = models.CharField(max_length=200)
    info = models.TextField(default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)