from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path("create_review/<int:ticket_id>/", views.create_review, name="create_review"),
    path("user_posts/", views.user_posts, name="user_posts"),
    path("edit_review/<int:review_id>/", views.edit_review, name="edit_review"),
    path("delete_review/<int:review_id>/", views.delete_review, name="delete_review"),
    path("edit_ticket/<int:ticket_id>/", views.edit_ticket, name="edit_ticket"),
    path("delete_ticket/<int:ticket_id>/", views.delete_ticket, name="delete_ticket"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("unfollow/<int:user_id>/", views.unfollow, name="unfollow"),
    path("user_search/", views.user_search, name="user_search"),
    path("accounts/", include("django.contrib.auth.urls")),
]
