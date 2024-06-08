# Steps to setup and run project locally
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
