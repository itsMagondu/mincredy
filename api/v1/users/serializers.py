from rest_framework import serializers

from api.v1.users.models import User, LoanLimit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'phone_number', 'country', 'occupation')


class LoanLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanLimit
        fields = ('user', 'loan_limit')
