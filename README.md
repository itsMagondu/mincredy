# INTRODUCTION
## Minicredy is a simple django API that connects to a json file instead of the normal ORM connection to a database.


# DESCRIPTION

## The following api endpoints are supported.

| Endpoint                 | HTTP Method | CRUD Method | Result              |   |
|--------------------------|-------------|-------------|---------------------|---|
| /api/v1/users/           | GET         | READ        | Get all users       |   |
| /api/v1/users/           | POST        | CREATE      | Add a user          |   |
| /api/v1/users/<int: id>/ | GET         | READ        | Get a specific user |   |
| /api/v1/users/<int: id>/ | PUT         | UPDATE      | Edit a user         |   |
| /api/v1/users/<int: id>/ | DELETE      | DELETE      | Delete a user       |   |
| /api/v1/loans/           | GET         | READ        | Get all loans       |   |
| /api/v1/loans/           | POST        | CREATE      | Add a loan          |   |
| /api/v1/loans/<int: id>/ | GET         | READ        | Get a specific user |   |
| /api/v1/loans/<int: id>/ | PUT         | UPDATE      | Edit a loan         |   |
| /api/v1/loans/<int: id>/ | DELETE      | DELETE      | Delete a loan       |   |



# Getting Started

Clone this repository\
Navigate to the main folder\
Create a virtual environment\
Activate the Virtual environment\
Install all the requirements\
\
The steps are shown below


```bash
git clone https://github.com/kimengu-david/mincredy
cd mincredy
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 

```

\
Perform all the migrations this is due to jwt authentication that is in use.
```bash
python manage.py migrate
```
\
Start your project
```bash
python manage.py runserver
```

# Examples
## Getting a specific user from the json file.
### step: 1

In this example we will use curl to make our requests, you could as well use httpie or use a different client like postman.

Run the following command to get your bearer token.

```bash
$ BearerToken=$(curl -s -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' --data '{"username":"david","password":"save"}' http://127.0.0.1:8000/api/token/|python3 -c "import sys, json; print(json.load(sys.stdin)['access'])")

```
### step: 2
make a request to the database using the Bearer token from the above step.

```bash
$ curl -H 'Accept: application/json' -H "Authorization: Bearer ${BearerToken}" http://127.0.0.1:8000/api/v1/users/1/;echo ""

```

## Getting all the users from a json file.
Use the previously generated bearer token to make your requests.

```bash
curl -H 'Accept: application/json' -H "Authorization: Bearer ${BearerToken}" http://127.0.0.1:8000/api/v1/users/;echo ""
```

## Getting a specific user from a json file.
```bash
curl -H 'Accept: application/json' -H "Authorization: Bearer ${BearerToken}" http://127.0.0.1:8000/api/v1/users/1/;echo ""

```
## Adding a user to the json file.
```bash
curl -X POST -H "Authorization: Bearer ${BearerToken}" -H "Content-Type: application/json" -d '{
    "id": 0,
    "firstname": "Ambitious",
    "lastname": "Johnson",
    "phone_number": "0713434342",
    "occupation": "teacher",
    "nationality": "Kenyan",
    "age": 30,
    "loan_limit": "ksh.200"
}' http://127.0.0.1:8000/api/v1/users/ ; echo""

```
## Getting all the loans from the json file.
```bash
curl -H 'Accept: application/json' -H "Authorization: Bearer ${BearerToken}" http://127.0.0.1:8000/api/v1/loans/;echo ""
```

## Getting a specific loan from the json file.
```bash
curl -H 'Accept: application/json' -H "Authorization: Bearer ${BearerToken}" http://127.0.0.1:8000/api/v1/loans/1/;echo ""


```