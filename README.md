## Description

This Django project aims to provide models and an API for handling JSON data in a specific format. The goal is to parse the data securely and offer the following endpoints for convenient data access. The code is written with the assumption that it will be read by others, ensuring robust error handling in case of incorrect data formats.


## Installation

1. Clone the repository:
    ```shell
    git clone https://github.com/malekjakub69/django_app.git
    ```

2. Install the dependencies into virtual environment:
    ```shell
    python -m venv venv 
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Apply database migrations:
    ```shell
    python manage.py migrate
    ```

## Run

1. Start the development server:
    ```shell
    python manage.py runserver
    ```

2. Access the API at `http://localhost:8000/`.

## API Endpoints



### Endpoints

* [POST] /import - This endpoint receives data and parses it.
* [GET] /detail/<model_name>/ - Retrieves a list of records based on the model name.
* [GET] /detail/<model_name>/<id> - Retrieves all data for a specific record.
