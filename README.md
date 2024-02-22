# Awesome House Style Project

Project for the management of online furniture store written on Django.


### Installing using GitHub

- Python3 must be already installed

```shell
git clone https://github.com/Viktor-Beniukh/awesome-house-style.git
cd awesome-house-style
python3 -m venv venv
source venv/bin/activate
pip install poetry
poetry install
python manage.py migrate
python manage.py runserver   
```

You need to create `.env.prod` file and add there the variables with your according values:
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;
- `DJANGO_DEBUG=False`;

- `EMAIL_HOST_USER`: this is email of sender, created on smtp server;
- `EMAIL_HOST_PASSWORD`: this is password of application, created on smtp server;
- `DEFAULT_FROM_EMAIL`: this is email of sender;
- `EMAIL_PORT`: this is port of smtp server;
- `EMAIL_HOST`: this is smtp server;

- `STRIPE_PUBLIC_KEY` & `STRIPE_SECRET_KEY`: your keys received after registration on the Stripe website;
- `BASE_URL`: base url to redirect after successful order payment or cancellation of its payment


To check functionality of the project without docker, you need to create directory `media`, and also to create
`.env` file and add there the variables with your according values:

- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;
- `DJANGO_DEBUG=True`;

- `EMAIL_HOST_USER`: this is email of sender, created on smtp server;
- `EMAIL_HOST_PASSWORD`: this is password of application, created on smtp server;
- `DEFAULT_FROM_EMAIL`: this is email of sender;
- `EMAIL_PORT`: this is port of smtp server;
- `EMAIL_HOST`: this is smtp server;

- `STRIPE_PUBLIC_KEY` & `STRIPE_SECRET_KEY`: your keys received after registration on the Stripe website;
- `BASE_URL`: base url(localhost) to redirect after successful order payment or cancellation of its payment



## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up`



## Features

- Powerful admin panel for advanced managing;
- Managing categories, products, orders, carts, reviews, ratings and users directly from website;
- Creating categories, products of store (only admin);
- Adding products to cart and creating orders;
- Adding products to favorite;
- Updating products data and removing products (only admin);
- Filtering of products by discount and categories;
- Sorting of products by prices;
- Searching of products by name and description;
- There is an opportunity to leave reviews for products (for authenticated users);
- It is possible to evaluate products by rating (for authenticated users);
- Registration and authorisation of users, creating and updating user profiles;
- Changing and reset user password.
    
  
### How to create superuser

- Run `docker-compose up` command, and check with `docker ps`, that services are up and running;
- Create new admin user. Enter container `docker exec -it <container_name> bash`, and create in from there;



## Testing

- Run tests using different approach: `docker-compose exec <container_name> "python manage.py test"`. (Container must be started) 
  


## Check project functionality

Superuser credentials for test the functionality of this project:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.
