# Airport API
API service for airport management writen on DRF

# Features
* JWT authenticated
* Customized admin panel /admin/
* Documentation is located at /api/doc/swagger-ui/
* Managing orders, flights, airplanes, routes, crew, airports as admin
* Searching flights as anonymous user and create orders as authenticated user
* Filtering and validation of tickets data
* Email based authorization (username replacement)

# Installing using GitHub
Install PostgresSQL and create database
> git clone https://github.com/lilarin/airport-api-service.git
> 
> cd airport_API
> 
> python -m venv venv
> 
> source venv/bin/activate
> 
> pip install -r requirements.txt
> 
> Create and fill .evn file using .env.template
> 
> python manage.py migrate
> 
> python manage.py runserver

# Run with Docker
Docker should be installed
> docker-compose build
> 
> docker-compose up

### Getting access
* create user via /api/user/register
* get access token via /api/user/token/
* renew token, if needed via /api/user/token/refresh/
