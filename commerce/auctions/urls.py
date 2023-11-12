from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:item>", views.details, name="listing"),
    path("listing/<int:item>/watchlist/<str:action>", views.watchlist, name="watchlist"),
    path("listing/<int:item>/closebid", views.closeBid, name="close"),
    path("listing/watchlist/<int:userNum>", views.userWatchlist, name="userWatchlist"),
    path("listing/category", views.category, name="category"),
    path("listing/category/<int:catId>", views.categoryListings, name="categoryListings"),
    path("listing/<int:item>/comment", views.comment, name="comment"),
]
