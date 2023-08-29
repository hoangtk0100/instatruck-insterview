from django.core.management.base import BaseCommand
from random import randint
from django.db import connection
from datetime import datetime, timedelta
from util.constants import DDMMYYY

class Command(BaseCommand):
    help = 'Initialize sample data for Directors, Actors, and Movies'

    def handle(self, *args, **options):
        self.initialize_data()

    def initialize_data(self):
        with connection.cursor() as cursor:
            self.insert_directors(cursor)
            self.insert_actors(cursor)
            self.insert_movies(cursor)

    def random_date(self):
        start_date = datetime(1900, 1, 1)
        end_date = datetime.now()
        random_date = start_date + timedelta(days=randint(0, (end_date - start_date).days))
        formatted_date = random_date.strftime(DDMMYYY)
        return formatted_date

    def insert_directors(self, cursor):
        # Create 10 Director records
        directors = []
        for i in range(1, 11):
            director = {
                'id': i,
                'name': f'Director {i}',
                'date': self.random_date(),
                'place': 'Some Place',
                'masterpiece': 'Some Masterpiece',
                'award_win': randint(0, 10),
                'award_nom': randint(0, 10),
                'person_link': f'https://person-{i}.com',
                'award_link': f'https://award-{i}.com',
            }
            directors.append(director)

        cursor.executemany(
            """
            INSERT INTO pages_director (id, name, date, place, masterpiece, award_win, award_nom, person_link, award_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [(director['id'], director['name'], director['date'], director['place'], director['masterpiece'],
            director['award_win'], director['award_nom'], director['person_link'], director['award_link'])
            for director in directors]
        )

    
    def insert_actors(self, cursor):
        # Create 10 Actor records
        actors = []
        for i in range(1, 11):
            actor = {
                'id': i,
                'name': f'Actor {i}',
                'date': self.random_date(),
                'place': 'Some Place',
                'masterpiece': 'Some Masterpiece',
                'award_win': randint(0, 10),
                'award_nom': randint(0, 10),
                'person_link': f'https://person-{i}.com',
                'award_link': f'https://award-{i}.com',
            }
            actors.append(actor)

        cursor.executemany(
            """
            INSERT INTO pages_actor (id, name, date, place, masterpiece, award_win, award_nom, person_link, award_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [(actor['id'], actor['name'], actor['date'], actor['place'], actor['masterpiece'],
            actor['award_win'], actor['award_nom'], actor['person_link'], actor['award_link'])
            for actor in actors]
        )

    def insert_movies(self, cursor):
        # Create 10 Movie records with relations to Director and Actor
        movies = []
        for i in range(1, 11):
            movie = {
                'id': i,
                'year': 2000 + i,
                'rank': i,
                'title': f'Movie {i}',
                'description': f'Description for Movie {i}',
                'duration': randint(90, 180),
                'genres': 'Action, Drama',
                'rating': 7.5 + i / 10,
                'metascore': 70 + i,
                'votes': randint(1000, 10000),
                'gross_earning_in_mil': 10 + i,
                'director_id': i,
                'actor_id': i,
            }
            movies.append(movie)

        cursor.executemany(
            """
            INSERT INTO pages_movie (id, year, rank, title, description, duration, genres, rating, metascore, votes, gross_earning_in_mil, director_id, actor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [(movie['id'], movie['year'], movie['rank'], movie['title'], movie['description'], movie['duration'],
            movie['genres'], movie['rating'], movie['metascore'], movie['votes'], movie['gross_earning_in_mil'],
            movie['director_id'], movie['actor_id'])
            for movie in movies]
        )