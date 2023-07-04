from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['GET'])
    def by_user(self, request):
        user_id = request.query_params.get('user_id')
        books = self.get_queryset().filter(user__id=user_id)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)