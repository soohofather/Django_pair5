from django.shortcuts import render, redirect, get_object_or_404

# 회원가입 form import
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

# login, logout 내장 form import
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# 회원인증
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# 메시지알림
from django.contrib import messages

# 로그인되어야지만 들어가지게 설정
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    user = get_user_model().objects.all()
    context = {"user": user}
    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ModelForm의 save 메서드의 리턴값은 해당 모델의 인스턴스다!
            auth_login(request, user)  # 로그인
            return redirect("reviews:index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    context = {"user": user}
    return render(request, "accounts/detail.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "reviews:index")
    else:
        form = AuthenticationForm
    context = {"form": form}
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    messages.warning(request, "로그아웃 하였습니다.")
    return redirect("reviews:index")


def follow(request, pk):
    # 프로필에 해당하는 유저를 로그인한 유저가!
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.user == user:
        messages.warning(request, "스스로 팔로우 할 수 없습니다.")
        return redirect("accounts:detail", pk)
    if request.user in user.followers.all():
        # (이미) 팔로우 상태이면, '팔로우 취소'버튼을 누르면 삭제 (remove)
        user.followers.remove(request.user)
    else:
        # 팔로우 상태가 아니면, '팔로우'를 누르면 추가 (add)
        user.followers.add(request.user)
    return redirect("accounts:detail", pk)
