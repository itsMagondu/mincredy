import json
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test import Client


base_url = "http://127.0.0.1:8000/api/v1"


class UserTests(APITestCase):
    """
        Contains all the methods that perform tests on the json file
    """
    # user_id and loan_id initialized to a non-existent values before execution.
    user_id = -1
    loan_id = -1

    @classmethod
    def setUpClass(cls):
        """
            Ensure all the test requests to the api endpoints are authenticated.
        """
        cls.user = User.objects.create_user(
            'test', 'test@cred.net', 'test')
        data = {"username": "test", "password": "test"}
        cls.client = Client()

        url = "http://127.0.0.1:8000/api/token/"
        response = cls.client.post(url, format='json', data=data)
        cls.token = json.loads(response.content.decode("utf-8")).get("access")

        cls.headers = {"HTTP_AUTHORIZATION": f"Bearer {cls.token}",
                       "HTTP_ACCEPT": "application/json"}

    def test_login(self):
        """
            Ensure the created mock user can login
        """
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)

    def test_get_all_users(self):
        """
        Ensure we get all the users from the json file
        """
        url = base_url + "/users/"
        response = self.client.get(url, **self.headers)
        #response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        with open("api/v1/users/users.json", 'r') as jsonfile:
            json_data = json.loads(jsonfile.read())
        self.assertEqual(json.loads(
            response.content), json_data)

    def test_add_user(self):
        """
        Ensure we can add a user to the json file.
        """
        url = base_url + "/users/"
        data = {
            "id": 0,
            "firstname": "Ambitious",
            "lastname": "Johnson",
            "phone_number": "0713434342",
            "occupation": "teacher",
            "nationality": "Kenyan",
            "age": 30,
            "loan_limit": "ksh.200"
        }
        response = self.client.post(
            url, data=data, **self.headers, format='json')
        self.assertEqual(response.status_code, 200)
        UserTests.user_id = json.loads(response.content)
        self.assertEqual(json.loads(
            response.content), UserTests.user_id)

    def test_get_specific_user(self):
        """
        Ensure we can get a specific user from the json file.
        """
        url = base_url + "/users/"+str(UserTests.user_id)+"/"
        response = self.client.get(url, **self.headers)
        self.assertEqual(json.loads(response.content), {
            "id": UserTests.user_id,
            "firstname": "Ambitious",
            "lastname": "Johnson",
            "phone_number": "0713434342",
            "occupation": "teacher",
            "nationality": "Kenyan",
            "age": 30,
            "loan_limit": "ksh.200"
        })

    def test_edit_user(self):
        """
        Ensure we can edit a specific user in the json file.
        """

        url = base_url + "/users/"+str(UserTests.user_id) + "/"
        data = {
            "firstname": "Ambitious",
            "lastname": "Johnson"
        }
        response = self.client.put(url, data=data, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(
            response.content), {

                "id": UserTests.user_id,
                "firstname": "Ambitious",
                "lastname": "Johnson",
                "phone_number": "0713434342",
                "occupation": "teacher",
                "nationality": "Kenyan",
                "age": 30,
                "loan_limit": "ksh.200"})

    def test_remove_user(self):
        """
        Ensure we can remove a specifc user from the json file.
        """
        url = base_url + "/users/"+str(UserTests.user_id) + "/"
        response = self.client.delete(url, **self.headers)
        self.assertEqual(json.loads(response.content),
                         "message: user deleted")

    def test_get_all_loans(self):
        """
        Ensure we can get all the loan objects from a json file.
        """
        url = base_url + "/loans/"
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_add_loan(self):
        """
        Ensure we can add a loan to the json file.
        """
        url = base_url + "/loans/"
        data = {
            "id": -1,
            "user_id": 3,
            "loan_amount": "ksh.300",
            "days": 30,
            "loan_status": "npl"
        }
        response = self.client.post(
            url, data=data, **self.headers, format='json')

        UserTests.loan_id = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(
            response.content), UserTests.loan_id)

    def test_edit_loan(self):
        """
            Ensure we can edit a specific loan in the json file.
        """

        url = base_url + f"/loans/{UserTests.loan_id}/"
        data = {
            "loan_status": "settled"
        }
        response = self.client.put(
            url, data=data, **self.headers, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(
            response.content), {
            "id": UserTests.loan_id,
            "user_id": 3,
            "loan_amount": "ksh.300",
            "days": 30,
            "loan_status": "settled"
        })

    def test_get_specific_loan(self):
        """
        Ensure we can get a specif loan in the json file.
        """
        url = base_url + f"/loans/{UserTests.loan_id}/"
        response = self.client.get(url, **self.headers)
        self.assertEqual(json.loads(response.content), {
            "id": UserTests.loan_id,
            "user_id": 3,
            "loan_amount": "ksh.300",
            "days": 30,
            "loan_status": "settled"
        })

    def test_remove_loan(self):
        """
        Ensure we can remove a specific loan from the json file.
        """
        url = base_url + f"/loans/{UserTests.loan_id}/"
        response = self.client.delete(url, **self.headers)
        self.assertEqual(json.loads(response.content),
                         "message: loan deleted")

    @classmethod
    def tearDownClass(cls):
        pass
