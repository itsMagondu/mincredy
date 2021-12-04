"""
    This module interacts with  data saved in a json file
    as per the user requests.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
from rest_framework.permissions import IsAuthenticated

from minicredy.settings import FILE_PATH


user_fields = ["firstname", "lastname", "phone_number",
               "occupation", "nationality", "age", "loan_limit"]
loan_fields = ["loan_amount", "days", "loan_status"]


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def all_users(request) -> Response:
    """
        Lists all the users from a json file or Adds a user to
        the json file depending on type of request.

        parameters: request - A request object
        Return: A Response object.

    """
    if request.method == "GET":
        # Retriving all the users from a json file.
        with open(FILE_PATH, 'r') as jsonfile:
            json_data = json.loads(jsonfile.read())
        return Response(json_data)

    if request.method == "POST":
        # Adding a user object to a json file.
        with open(FILE_PATH, 'r') as jsonfile:
            json_data = json.loads(jsonfile.read())
        # The user_id of the newly added user will be the last item in the list
        # of users
        user_id = len(json_data["users"]["user_details"])+1
        request.data["id"] = user_id
        json_data["users"]["user_details"].append(request.data)
        with open(FILE_PATH, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
        return Response(user_id)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def manage_user(request, id) -> Response:
    """
        Gets a specific user from a json file or Edits a specific user in a 
        json file, or deletes a specific user in a json file depending on the
        type of request.

        parameters: request - a python request object.
                    id - A unique id of a user in a database.
        Return: On success - The requested user or edited user or a success delete message.
                on fail  - User does Not exists

    """
    with open(FILE_PATH, 'r') as jsonfile:
        json_data = json.loads(jsonfile.read())
    try:
        user = json_data.get("users").get("user_details")[id-1]
    except:
        return Response("User does Not exist")
    if request.method == "GET":
        return Response(user)

    if request.method == "PUT":
        # Editing a user object instance in the json file.
        for field in user_fields:
            field_value = request.data.get(field)
            if field_value is not None:
                user[field] = field_value
        # The value of the user_details in the json file is a list hence we subtract 1
        json_data["users"]["user_details"][id-1] = user
        with open(FILE_PATH, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
        return Response(user)

    if request.method == "DELETE":
        # removing a user object instance in a json file.
        json_data["users"]["user_details"].pop(id-1)
        with open(FILE_PATH, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
        return Response("message: user deleted")


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def all_loans(request) -> Response:
    """
        Lists all the loans from a json file or adds a new loan depending
        on type of user request.

        parameters: request - A python request object.
        Return: A python response object.

    """
    if request.method == "GET":
        # Retrieving all the loans from a json file.
        with open(FILE_PATH, 'r') as jsonfile:
            json_data = json.loads(jsonfile.read())
        return Response(json_data.get("users").get("all_loans"))

    if request.method == "POST":
        # Adding a loan object to the json file.
        with open(FILE_PATH, 'r') as jsonfile:
            json_data = json.loads(jsonfile.read())
        loan_id = len(json_data["users"]["all_loans"])+1
        request.data["id"] = loan_id
        json_data["users"]["all_loans"].append(request.data)
        with open(FILE_PATH, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
        return Response(loan_id)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def manage_loan(request, id) -> Response:
    """
        Gets a specific loan from a json file or Edits a specific loan in a 
        json file, or deletes a specific loan in a json file depending on the
        type of request.

        parameters: request - a python request object.
                    id - A unique id of a loan in a database.
        Return: On success - The requested loan or edited loan or a success delete message.
                on fail  - Loan does Not exists

    """
    with open(FILE_PATH, 'r') as jsonfile:
        json_data = json.loads(jsonfile.read())
    try:
        loan = json_data.get("users").get("all_loans")[id-1]
    except:
        return Response("Loan does Not exist")
    if request.method == "GET":
        return Response(loan)

    if request.method == "PUT":
        # Editing a loan object in the json file.
        for field in loan_fields:
            field_value = request.data.get(field)
            if field_value is not None:
                loan[field] = field_value
        json_data["users"]["all_loans"][id-1] = loan
        with open(FILE_PATH, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
        return Response(loan)

    if request.method == "DELETE":
        # Deleting a loan object in the database.
        json_data["users"]["all_loans"].pop(id-1)
        with open(FILE_PATH, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
        return Response("message: loan deleted")
