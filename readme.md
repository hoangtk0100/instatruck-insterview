# Instatruck coding test

Small coding tests to evaluate development skills.

## Python test Goal

The `instatest.py` file contains a class, a mock and some basic tests. The candidate should:

 * Fork the project
 * Read and understand the Wrapper class
 * Using your test framework of choice, write some additional tests, including at least one to ensure that values written to the file cache are re-read correctly
 * Refactor the Wrapper class in any way you see fit, to improve its structure, reliability, testability, maintainability, reusabilty and pythonic-ness.

The aim is to understand your ability and pragmaticness of writing, testing and maintaining python code. The only rules in addition to the above are:

 * Python3 should be used
 * executing `python -m instatest` should not fail.
 * any tests should be able to be run with a single command in the root repository folder.

## Django test goal

In the folder 'django', there is a django project which runs in a docker container. From inside the `django` folder, the docker container can be built with:

`docker build -t movietest .`

and run with:

`docker run -v ${PWD}:/opt/project -p 8000:8000 movietest python3 manage.py runserver 0.0.0.0:8000`

The django project is currently not working because:

 * it does not use the sqlite database correctly (instead it reads CSV files which are now missing)
 * it represents a full-stack solution, but we want to convert it to an API

### 1. Convert to API which reads the sqlite database

Modify the django project to use Django Rest Framework to convert the project into an API which provides the following endpoints:

  - `/movies/` lists all movies in the database with the fields 'title', 'year', 'description', 'rating'
  - `/actors/` lists all actors in the database with the fields 'name', 'birthdate' and 'birthplace', and a 'films' field which is a URL
  - `/actors/<id>/films/` lists the films for actor <id>, which matches the 'films' url link in the actors information
  - `/directors/` lists all directors in the database with the fields 'name', 'birthdate' and 'birthplace', and a 'films' field which is a URL link
  - `/directors/<id>/films/` lists the films for director <id>, which matches the 'films' url link in the directors information

### 2. Implement filtering user requirement

User Story:

```
As an API user
I want to filter movies by year
So that I can find movies I want more easily
```

BDD Scenarios:
```
GIVEN I am using the movie API
WHEN I provide a 'start year' value to the `/movies/` endpoint
THEN the API only shows me movies from the 'start year' and later

GIVEN I am using the movie API
WHEN I provide a 'end year' value to the `/movies/` endpoint
THEN the API only shows me movies before and including the 'end year'

GIVEN I am using the movie API
WHEN I provide a 'start year' value and a 'end year' value to the `/movies/` endpoint
THEN the API only shows me movies between and including 'start year' and 'end year'
```

Implement the scenarios above, including passing tests. Include handling and tests for invalid inputs which you think are necessary.

### 3. Implement a top-10 user requirement

User Story:

```
As an API user
I want to know the highest rated movies
So that I can choose a good movie more easily
```

BDD Scenario:
```
GIVEN I am using the movie API
WHEN I access the '/movies/best/<n>' endpoint
THEN the API only shows me the movies <movielist> sorted by rating any then by metascore

EXAMPLES:
  | n | movielist                                |
  | 3 | The Dark Knight, Inception, Spider-Man: Into the Spider-Verse |
  | 5 | The Dark Knight, Inception, Spider-Man: Into the Spider-Verse, Interstellar, Whiplash |
```

Implement the scenarios above, including passing tests. Include handling and tests for invalid inputs which you think are necessary.

BONUS: Use a BDD-framework to test the BDD scenario.

### 4. Implement nearest-to-birthday requirement

User Story:

```
As a movie fan
I want to know which actors are born closest to me
So that I can learn some interesting information
```

 BDD Scenario:
```
GIVEN I am using the movie API
WHEN I access the `/actors/birthdays/<date>/` endpoint
THEN the API shows me the actor information for <actorname>

EXAMPLES:
  | date     | actorname |
  | 13031975 | Christina Hendricks |
  | 20081979 | Oscar Isaac |
  | 19091990 | Bill Skarsgård |
```

Implement the scenario above. Note that the date column has been poorly designed in the database, and so will require some manipulation.

## Delivery

The result should be provided as a GitHub pull request in a manner that identifies you. If you use any additional pip modules, they should be added to the requirements file. If you wish to provide notes, you may do so either in a markdown file or in comments, whichever you feel is more appropriate.


