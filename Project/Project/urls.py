from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.Login, name="login"),
    path("logout", views.Logout, name="logout"),
    path("register", views.Register, name="register"),
    path("conversations", views.filmConversation, name="fcon"),
    path("stream/<int:id>", views.stream, name="stream"),
    path("films", views.films, name="films"),
    path("genre/<int:id>", views.genrefilm, name="genre"),
    path("userarea", views.userarea, name="userarea"),
    path("updateusername", views.updateusername, name="updateusername"),
    path("updateemail", views.updateemail, name="updateemail"),
    path("updatepassword", views.updatepassword, name="updatepassword"),
    path("submitreview", views.submitreview, name="submitreview"),
    path("publishfilm", views.publishfilm, name="publishfilm"),
    path("favorites", views.favorites, name="favorites"),
    path("allgenres", views.allgenres, name="allgenres"),
    path("favorite", views.favorite, name="favorite"),
    path("queryfilm", views.queryfilm, name="queryfilm"),
    path("updatefilm/<int:id>", views.updatefilm, name="updatefilm"),
    path("updatereview/<int:id>", views.updatereview, name="updatereview"),
    path("uploaded", views.uploaded, name="uploaded"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)