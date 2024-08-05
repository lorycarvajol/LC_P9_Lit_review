from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "reviews/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "reviews/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "reviews/logout.html")


@login_required
def home(request):
    tickets = Ticket.objects.all().order_by("-time_created")
    reviews = Review.objects.all().order_by("-time_created")
    context = {
        "tickets": tickets,
        "reviews": reviews,
    }
    return render(request, "reviews/home.html", context)


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")
    else:
        form = TicketForm()
    return render(request, "reviews/create_ticket.html", {"form": form})


@login_required
def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("home")
    else:
        form = ReviewForm()
    return render(request, "reviews/create_review.html", {"form": form})


@login_required
def create_review_response(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
    else:
        form = ReviewForm()
    return render(
        request, "reviews/create_review_response.html", {"form": form, "ticket": ticket}
    )


@login_required
def user_posts(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    return render(
        request,
        "reviews/user_posts.html",
        {"user_tickets": user_tickets, "user_reviews": user_reviews},
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("user_posts")
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/edit_review.html", {"form": form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        review.delete()
        return redirect("user_posts")
    return render(request, "reviews/confirm_delete.html", {"object": review})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("user_posts")
    else:
        form = TicketForm(instance=ticket)
    return render(request, "reviews/edit_ticket.html", {"form": form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        return redirect("user_posts")
    return render(request, "reviews/confirm_delete.html", {"object": ticket})


@login_required
def subscriptions(request):
    search_query = request.GET.get("search", "")
    search_results = []
    if search_query:
        search_results = User.objects.filter(username__icontains=search_query).exclude(
            username=request.user.username
        )

    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user_to_follow = User.objects.get(username=username)
            if user_to_follow != request.user:
                UserFollows.objects.get_or_create(
                    user=request.user, followed_user=user_to_follow
                )
        except User.DoesNotExist:
            pass

    subscriptions = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)

    return render(
        request,
        "reviews/subscriptions.html",
        {
            "subscriptions": subscriptions,
            "followers": followers,
            "search_results": search_results,
            "search_query": search_query,
        },
    )


@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    UserFollows.objects.filter(
        user=request.user, followed_user=user_to_unfollow
    ).delete()
    return redirect("subscriptions")


@login_required
def user_search(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        query = request.GET.get("term", "")
        users = User.objects.filter(username__icontains=query).exclude(
            username=request.user.username
        )
        results = [
            {"id": user.id, "label": user.username, "value": user.username}
            for user in users
        ]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)
