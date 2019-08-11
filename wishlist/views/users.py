from rest_framework.decorators import api_view
from rest_framework.response import Response

from wishlist.serializer import RegistrationSerializer


@api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=200)


@api_view(['POST'])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)
