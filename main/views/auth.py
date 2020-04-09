from rest_framework.views import APIView
from rest_framework.response import Response
from main.serializers import UserSerializerWithToken, UserSerializer
from rest_framework.decorators import api_view
from rest_framework import permissions, status
from django.core.exceptions import ValidationError


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)

        # It validates email
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            # If password is incorrect
            except ValidationError as exc:
                return Response(exc.message_dict, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
