# Steps for running project with docker-compose
- These instructions are for Ubuntu based machines.

After cloning the project, 

#### 1. Build docker image with
    docker-compose build
#### 2. Start the container with
    docker-compose up
#### 3. Create superuser with 
    docker-compose run accuknox_coding_assignment python manage.py createsuperuser
After the setup, test the APIs with postman.

### Note: In case if you are getting permission error while executing docker-entrypoint.sh, fix it with
    chmod +x docker_entry_point.sh


# Steps for running the project locally

- These instructions are for Ubuntu based machines.

After cloning the project,

#### 1. Create a virtualenv and install dependencies with

    pip install -r requirements.txt

#### 1. Create a .env file with the provided template .env_template and fill the values accordingly

#### 3. run make migrations and migrate command and create cache table

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createcachetable

#### 4. Create superuser with

    python manage.py createsuperuser

#### 5. Run the project with:
    python manage.py runserver


## -Note:
1. This project uses default sqlite3 db as it is a coding assignment and I haven't used Postgres/MySQL.
2. DB based caching is used.
3. If you find any errors while running the project or any other queries, then please reach out.


