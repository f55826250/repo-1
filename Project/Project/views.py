from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.utils import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
import json

# Create your views here.

# base home view
@cache_page(60 * 10)
def index(request):
  return render(request, "Project/index.html")

# basic user system
def Login(request):
  if request.method == "GET":
    return render(request, "Project/login.html")
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      print("logged")
      return redirect(reverse("index"))
    return redirect(reverse("index"))

def Register(request):
  if request.method == "GET":
    return render(request, "Project/register.html")
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    repassword = request.POST["repassword"]
    
    if password != repassword:
      print("password mismatch")
      return redirect(reverse("register")) 
    
    try:
      validate_email(email)
    except ValidationError:
      print("bademail")
      return redirect(reverse("register"))
    
    try:
      newuser = User.objects.create_user(username, email, password)
      newuser.save()
    except IntegrityError:
      print("bad username or password")
      return redirect(reverse("register"))
    
    user = authenticate(request, username=username, password=password)
    login(request, user)
    return redirect(reverse("index"))

def Logout(request):
  logout(request)
  return redirect(reverse("index"))

# film showing/filtering/queryng
def filmConversation (request):
  rf = Film.objects.all().order_by('?')[:2] 
  return render(request, "Project/fconversation.html", {
    "rfa":rf[0], 
    "rfb":rf[1],
  })

def stream(request, id):
  if request.method == "GET":
    film = Film.objects.get(pk=id)
    fav = False
    try:
      Favorite.objects.get(film = film, user = request.user)
      fav = True
    except:
      pass
    return render(request, "Project/stream.html", {
      "film":film,
      "reviews":Review.objects.filter(film=film),
      "favorite":fav
      })

def films(request):
  films = Film.objects.all()
  return render(request, "Project/films.html", {
    'films': films
    })

def genrefilm(request, id):
  films = Film.objects.filter(genre=Genre.objects.get(pk=id))
  return render(request, "Project/genrefilms.html", {
    "films": films,
    "genre": Genre.objects.get(pk=id).genre
    })

def allgenres(request):
  genres = []
  for genre in Genre.objects.all():
    genres.append({genre.genre:genre.Films})

  return render(request, "Project/allgenres.html", {
  "genres": Genre.objects.all(),
  })

def queryfilm(request):
  if request.method == "POST":
    query = request.POST["query"]
    return render(request, "Project/queryfilm.html", {
      "films": Film.objects.raw("SELECT * FROM Project_film WHERE title LIKE %s", ["%"+query+"%"]),
      "query":query,
    })

@login_required
def favorites(request):
  films = []
  for fav in Favorite.objects.filter(user = request.user):
    films.append(fav.film)
  return render(request, "Project/favorites.html", {
  "films": films,
  })

# user section views
@login_required
@cache_page(60 * 10)
def userarea(request):
  return render(request, "Project/userarea.html")

def publishfilm(request):
  if request.method == "GET":
    return render(request, "Project/uploadfilm.html", {
      "genres":Genre.objects.all(),
    })
  if request.method == "POST":
    title = request.POST["title"]
    description = request.POST["description"]
    poster = request.FILES.get("poster")
    film = request.FILES.get("film")
    genre = request.POST.getlist('genres')
    if title == "" or description == "" or genre == "Choose a Genre":
      return redirect(reverse("publishfilm"))
    
    newfilm = Film(title=title, description=description, poster=poster, upload=film)
    newfilm.save()
    for gen in genre:
      newfilm.genre.add(Genre.objects.get(pk=int(gen)))
    newfilm.save()
    return redirect(reverse("index"))

# apis
@login_required
def updateusername(request):
  if request.method == "POST":
    errs = ""
    try:
      request.user.username = request.POST["newusername"]
      request.user.save()
    except:
      errs = "a user is arleady using this name"
  return render(request, "Project/userarea.html", {
    "errs": errs
  })

@login_required
def updateemail(request):
  if request.method == "POST":
    email = request.POST["newemail"]
    errs = ""
    try:
      validate_email(email)
      request.user.email = email
      request.user.save()
    except ValidationError:
      errs = "the email is not valid"
    
    print("test"+errs)
    return render(request, "Project/userarea.html", {
      "errs": errs
    })

@login_required
def updatepassword(request):
  if request.method == "POST":
    password = request.POST["newpassword"]
    request.user.set_password(password)
    request.user.save()
  return redirect(reverse("userarea"))

@login_required
def submitreview(request):
  if request.method == "PUT":
    data = json.loads(request.body)
    review = data.get("revBody")
    rating = int(data.get("rating"))
    pk = data.get("pk")
    print(rating, review, pk)
    if rating >= 0 and rating <= 10:
      try:
        rev = Review(film = Film.objects.get(pk=pk), user = request.user, body = review, rating = rating)
        rev.save()
      except:
        pass
    return render(request, "Project/userarea.html")

# method via put that add/remove a film from favorites
@login_required
def favorite(request):
  if request.method == "PUT":
    data = json.loads(request.body)
    pk = data.get("pk")
    # searches for other equals followings, if hit delete else remove
    if Favorite.objects.filter(user=request.user, film=Film.objects.get(pk=pk)).__len__() == 0:
      newfav = Favorite(user=request.user, film=Film.objects.get(pk=pk))
      newfav.save()
    else:
      oldfav = Favorite.objects.get(user=request.user, film=Film.objects.get(pk=pk))
      oldfav.delete()
    return render(request, "Project/userarea.html")

# method via POST update a film data
# method via GET renders the update film HTML
@login_required
def updatefilm(request, id):
  if request.method == "GET":
    film = Film.objects.get(pk=id)
    if request.user == film.author:
      selectedg = film.genre.all()
      unselectedg = []
      for genre in Genre.objects.all():
        if not (genre in selectedg):
          unselectedg.append(genre)
      return render(request, "Project/updatefilm.html", {
        "title": film.title,
        "description": film.description,
        "selected": selectedg,
        "unselectedg": unselectedg,
        "id":id
      })
    else:
      return redirect(reverse("userarea"))
  
  if request.method == "POST":
    if request.user == Film.objects.get(pk = id).author:
      # get all the contents of the form
      title = request.POST["title"]
      description = request.POST["description"]
      poster = request.FILES.get("poster")
      genre = request.POST.getlist('genres')
      # update the film data
      film = Film.objects.get(pk = id)
      film.title = title
      film.description = description
      film.poster = poster
      film.genre.clear()
      for gen in genre:
        film.genre.add(Genre.objects.get(pk=int(gen)))
      film.save()
      print(film.genre)
      return redirect(reverse("userarea"))
    else:
      return redirect(reverse("userarea"))

# method via POST update a review data
# method via GET renders the update review HTML
@login_required
def updatereview(request, id):
  if request.method == "GET":
    review = Review.objects.get(pk = id)
    if review.user == request.user:
      return render(request, "Project/updatereview.html", {
          "title": review.film.title,
          "reviewText": review.body,
          "rating": review.rating,
          "id":id
        })
    
  if request.method == "POST":
    review = Review.objects.get(pk = id)
    if review.user == request.user:
      rating = request.POST["rating"]
      reviewText = request.POST["reviewText"]
      review.rating = rating
      review.body = reviewText
      review.save()
      return redirect(reverse("userarea"))

@login_required
def uploaded(request):
  if request.method == "GET":
    return render(request, "Project/uploaded.html", {
      "films":Film.objects.filter(author = request.user),
      "reviews":Review.objects.filter(user = request.user),
    })