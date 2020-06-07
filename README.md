TESTAREA AUTOMATA - Web app

## Setup

Python - 3.8.1

Create virtual environment
```shell script
$ pip install virtualenv
$ virtualenv testarea_automata
```

Activate virtual environment
```shell script
$ source testarea_automata/bin/activate
```

Navigate to project directory
```shell script
(testarea_automata) $ cd web_platform
```

Install dependencies
```shell script
(testarea_automata) $ pip install -r requirements
```

## Development deployment

Set environment variables
```shell script
(testarea_automata) $ export DJANGO_SETTINGS_MODULE=web_platform.settings.development
```

Run server with gunicorn to access application in http://127.0.0.1:10001/
```shell script
(testarea_automata) $ python manage.py runserver 10001
```

## Production deployment

Set environment variables
```shell script
(testarea_automata) $ export SECRET_KEY='your secret key'
(testarea_automata) $ export DJANGO_SETTINGS_MODULE=web_platform.settings.production
```

Collect static files
```shell script
(testarea_automata) $ python manage.py collectstatic
```

Run server with gunicorn to access application in http://127.0.0.1:10001/
```shell script
(testarea_automata) $ gunicorn web_platform.wsgi -b :10001 --workers=3
```