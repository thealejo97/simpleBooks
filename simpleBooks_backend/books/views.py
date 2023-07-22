from rest_framework import viewsets
from .models import Book
import requests
from rest_framework.views import APIView
from .serializers import BookSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['GET'])
    def by_user(self, request):
        user_id = request.query_params.get('user_id')
        books = self.get_queryset().filter(user__id=user_id)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():


            if serializer.validated_data.get('finished'):
                serializer.validated_data['reading_status_porcentaje'] = 100
                serializer.validated_data['readed_pages'] = serializer.validated_data.get('total_pages')
            else:
                readed_pages = serializer.validated_data.get('readed_pages')
                total_pages = serializer.validated_data.get('total_pages')
                porcentaje_leido = int((readed_pages * 100) / total_pages)
                serializer.validated_data['reading_status_porcentaje'] = porcentaje_leido

            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("serilizer error, " , serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetRecommendedBooksName(APIView):
    def get(self, request):
        book_name = request.query_params.get('book_name', '')
        book_name = book_name.replace(' ', '+')
        url = f'https://openlibrary.org/search.json?q={book_name}&_spellcheck_count=0&limit=10&fields=key,cover_i,title,subtitle,author_name,name,isbn&mode=everything'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            books = data['docs']

            # Create a list to hold the book data
            recommended_books = []

            for book in books:
                book_info = {
                    'title': book.get('title', ''),
                    'author': ', '.join(book.get('author_name', [])),
                    'key_openlibrary': book.get('key', []),
                }
                if book.get('isbn', None):
                    isbn = book.get('isbn')[0]
                    # Get additional info using the Google Books API
                    google_books_data = self.obtener_info_google_books(isbn)
                    book_info['isbn'] = isbn
                    book_info['num_pages'] = google_books_data.get('pageCount', '')
                    book_info['published_date'] = google_books_data.get('publishedDate', '')
                    book_info['summary'] = google_books_data.get('description', '')
                    book_info['genre'] = google_books_data.get('categories', [])
                else:
                    book_info['isbn'] = ''
                    book_info['num_pages'] = ''
                    book_info['published_date'] = ''
                    book_info['summary'] = ''
                    book_info['genre'] = []

                recommended_books.append(book_info)
            recommended_books = sorted(recommended_books, key=lambda x: not x['summary'])

            return Response(recommended_books, status=200)
        else:
            return Response({'error': 'Error al obtener los datos del libro'}, status=500)

    def obtener_info_google_books(self, isbn):
        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                libro = data['items'][0]['volumeInfo']
                return libro
        return {}