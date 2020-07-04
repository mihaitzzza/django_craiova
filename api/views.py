from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from api.serializers import UsersSerializer, PublisherSerializer, RegisterSerializer
from library.models.publisher import Publisher
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

UserModel = get_user_model()


# class UsersViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = UserModel.objects.all()
#         serializer = UsersSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         user = get_object_or_404(UserModel, pk=pk)
#         serializer = UsersSerializer(user)
#         return Response(serializer.data)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.POST)

        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UsersSerializer(instance=user)
            return Response({
                'user': user_serializer.data
            })

        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)