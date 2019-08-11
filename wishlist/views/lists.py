from rest_framework import mixins, generics, permissions
from rest_framework.response import Response

from wishlist.models import List
from wishlist.serializer import ListSerializer, ProductDetailSerializer


class ListsList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset = List.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListSerializer

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.filter(user_id=request.user.id), many=True)
        return Response(serializer.data)

    def post(self, request):
        return self.create(request)


class ListDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = List.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListSerializer

    def get(self, request, pk):
        list = List.objects.get(id=pk)
        serializer = ProductDetailSerializer(list.products.values(), many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
