"""
URL configuration for simpleBooks_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from django.contrib import admin

from simpleBooks_backend.reading_sessions.views import ReadingSessionViewSet, ReadingSessionStatistics
from simpleBooks_backend.users.views import UserViewSet, CustomLoginView, CustomRegisterView
from simpleBooks_backend.books.views import BookViewSet
from simpleBooks_backend.authors.views import AuthorViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'reading_sessions', ReadingSessionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/books/by_user/', BookViewSet.as_view({'get': 'by_user'}), name='books-by-user'),
    path('api/readingsessin/getStadistics/', ReadingSessionStatistics.as_view(), name='getStadistics'),
    path('api/auth/login/', CustomLoginView.as_view(), name='rest_login'),
    path('api/auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
