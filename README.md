# backend_coderr

A RESTful backend service for the freelancer platform Coderr.


## Django Project

The project is called 'backend_coderr', but project files are stored in the 'core' folder. Please refer to 'core/settings.py' for further details.


## Requirements

+ Python 3.13
+ Django 5.2.4
+ SQLite 3


## Technologies

backend_coderr uses the following technologies and tools: 

![Python](	https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)     ![Django](https://img.shields.io/badge/Django-5.2.4-green?style=for-the-badge&logo=django&logoColor=white)     ![DjangoREST](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)     ![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite&logoColor=white)


## Django Apps

Apps include: 

+ auth_app - this is for signup and login logic that don't require a token or authenticated user and also to show the user profile of an authenticated user.
+ coderr_app - this is for the data models of Offers, Offer Details, Orders and Review and the logic for creating, updating, viewing and deleting data with different permissions. Can only be accessed by authenticated users.


## Database

The SQLite3 database used sits in the Django project root folder. It is not included within the Git repo, so must instead be requested from the system admin. 


## Settings

There is 1 settings related file:

+ `settings.py` (for general project settings, regardless of environment and containing publicly accessible information)


## Installation

Clone the repostiory:
```sh
git clone https://github.com/tinyjoe/backend_coderr.git
cd backend_coderr
```

Create a virtual environment
```sh
python -m venv env
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install dependencies
```sh
pip install -r requirements.txt
```

## Database Migrations

Run the initial migrations
```sh
python manage.py migrate
```

When you make changes to models
```sh
python manage.py makemigrations
python manage.py migrate
```

## Start Development Server
```sh
python manage.py runserver
```


## Frontend Setting
This backend was created for the frontend version 1.2.1.

## Guest Login Credentials
```js
const GUEST_LOGINS = {
  customer: {
    username: "DemoCustomer",
    password: "C-D3mo-P4ssw0rd",
  },
  business: {
    username: "DemoBusiness",
    password: "B-D3mo-P4ssw0rd",
  },
};
```

