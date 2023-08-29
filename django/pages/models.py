from django.db import models

# Create your models here.
class Director(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=500, null=True)
    masterpiece = models.CharField(max_length=500, null=True)
    award_win = models.IntegerField(blank=True, null=True, default=None)
    award_nom = models.IntegerField(blank=True, null=True, default=None)
    person_link = models.URLField(max_length=500, null=True, default=None)
    award_link = models.URLField(max_length=500, null=True, default=None)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthdate': self.date,
            'birthplace': self.place,
        }
    

class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=500, null=True)
    masterpiece = models.CharField(max_length=500, null=True)
    award_win = models.IntegerField(blank=True, null=True, default=None)
    award_nom = models.IntegerField(blank=True, null=True, default=None)
    person_link = models.URLField(max_length=500, null=True, default=None)
    award_link = models.URLField(max_length=500, null=True, default=None)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthdate': self.date,
            'birthplace': self.place,
        }


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField()
    rank = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500, null=True)
    duration = models.IntegerField(blank=True, null=True)
    genres = models.CharField(max_length=100)
    rating = models.FloatField(blank=True, null=True)
    metascore = models.IntegerField(blank=True, null=True, default=None)
    votes = models.IntegerField(blank=True, null=True)
    gross_earning_in_mil = models.FloatField(blank=True, null=True, default=None)
    director = models.ForeignKey(Director, to_field="id", db_column="director_id", related_name='movie_fk_director', on_delete=models.CASCADE, null=True, blank=True)
    actor = models.ForeignKey(Actor, to_field="id", db_column="actor_id", related_name='movie_fk_actor', on_delete=models.CASCADE, null=True, blank=True)

    def to_dict(self):
        return {
        'id': self.id,
        'title': self.title,
        'year': self.year,
        'description': self.description,
        'rating': self.rating,
    }