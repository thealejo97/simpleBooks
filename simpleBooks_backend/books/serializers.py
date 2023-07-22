from rest_framework import serializers
from .models import Book
from ..authors.models import Author
from ..authors.serializers import AuthorSerializer


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'ISBN',
            'publication_date',
            'publication_year',
            'total_pages',
            'creation_date',
            'resume',
            'genre',
            'cover_image',
            'author',
            'user',
            'readed_pages',
            'reading_status_porcentaje',
            'finished',
            'language'
        ]

    def to_representation(self, instance):
        self.fields['author'] = AuthorSerializer(read_only=True)
        return super().to_representation(instance)
