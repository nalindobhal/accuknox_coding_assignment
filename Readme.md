# Steps to setup and run project locally
After cloning the project, 

#### 1. Build docker image with
    docker-compose build
#### 2. Start the container with
    docker-compose up
#### 3. Create superuser with 
    docker-compose run accuknox_coding_assignment python manage.py createsuperuser
