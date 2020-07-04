from rest_framework import serializers
from django.contrib.auth import get_user_model
from library.models.publisher import Publisher

UserModel = get_user_model()


# class UsersSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     first_name = serializers.CharField(max_length=255)
#     last_name = serializers.CharField(max_length=255)
#     email = serializers.EmailField(max_length=255)
#     is_staff = serializers.BooleanField()
#     is_superuser = serializers.BooleanField()
#
#     def update(self, instance, validated_data):
#         pass
#
#     def create(self, validated_data):
#         pass

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ['password']


class PublisherSerializer(serializers.ModelSerializer):
    owner = UsersSerializer()

    class Meta:
        model = Publisher
        exclude = []


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)

    def validate_email(self, email):
        is_unique_email = UserModel.objects.filter(email=email).count() == 0
        if not is_unique_email:
            raise serializers.ValidationError('E-mail already exists.')

        return email

    def validate(self, data):
        errors = {}

        first_name = data.get('first_name', None)
        if not first_name:
            errors['first_name'] = ['This field is required.']

        last_name = data.get('last_name', None)
        if not last_name:
            errors['last_name'] = ['This field is required.']

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return data

    def save(self):
        user = UserModel.objects.create_user(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        return user
