## Features

*   support multiple elasticsearch clusters

*   manage hundreds or thousands of indices


## Installation


## Configuration

create a superuser

```
$ python manage.py createsuperuser
```

## Start Server

```
# cd to project_dir
$ python manage.py runserver 0.0.0.0:8000
$ celery -A elasticmanager worker --loglevel=INFO
$ celery beat -A elasticmanager --loglevel=INFO
```
