# elasticmanager
Manage Indices of Elasticsearch

## Requirements

*   Python 2.7, 3.3, 3.4, 3.5

*   (Optional) MySQL

If you don't want to use default sqlite database, you can configure to use mysql

## Getting Started

### Step 1 : Clone elasticmanager project

```
git clone https://github.com/InterestingLab/elasticmanager.git
```

### Step 2 : Install Dependencies

```
cd elasticmanager

pip install -r requirements/dev.txt
```

### Step 3 : Init Database

```
python manage.py migrate
```

### Step 4 : Start Application

```
# in project dir

# Start Web
python manage.py runserver 0.0.0.0:8080

# Start Celery Task Scheduler & Worker
celery -A elasticmanager worker --loglevel=INFO
celery beat -A elasticmanager --loglevel=INFO
```
