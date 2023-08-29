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