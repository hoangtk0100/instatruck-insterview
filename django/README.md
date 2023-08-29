# Movie DB


# Install
```
    make install
```


# Run
## 1. Initialize database tables
```
    make migrate
```

## 2. Initialize data
```
    # Method 1:
    make initdata
    make createsuperuser # then enter your user info
```

```
    # Method 2:
    make initdb

    # Default user
    # Username/Email: admin@mail.com
    # Password: admin0100
```

## 3. Run server
```
    make server
```

## 4. Backup database
```
    make backupdb
```

## 5. Restore database
```
    make restoredb
```

## 6. Create a new migration
```
    make makemigrations
```


# API docs - [Postman](static/docs/instatest.postman_collection.json)
| Method | Path                                       | Description              | Notes                                      |
| ------ | ------------------------------------------ | ------------------------ | ------------------------------------------ |
| GET    | `/movies?page=1&limit=10&start_year=2000`   | Filter movies            | Options: page, limit, start_year, end_year, actor_id, actor_name, director_id, director_name           |
| GET    | `/movies/best/:amount?page=2`               | Get best movies          | Options: page, limit, start_year, end_year, actor_id, actor_name, director_id, director_name, sort_by, sort_type |
| GET    | `/actors`                                  | List actors              |                                            |
| GET    | `/actors/:id/films`                        | List movies by actor     | Requires actor ID                         |
| GET    | `/actors/birthdays/:date`                  | Filter actors by birthday| Requires birthdate in the format          |
| GET    | `/directors`                               | List directors           |                                            |
| GET    | `/directors/:id/films`                     | List movies by director  | Requires director ID                      |
