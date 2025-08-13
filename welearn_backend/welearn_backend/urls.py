"""
URL configuration for welearn_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# welearn_backend/urls.py
from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('api/register/', views.RegisterView.as_view()),
    path('api/login/', views.login_view),
    path('api/current-user/', views.current_user),

    # users
    path('api/users/', views.UserListView.as_view()),
    path('api/users/<int:pk>/', views.UserDetailView.as_view()),

    # courses
    path('api/courses/', views.CourseListCreateView.as_view()),
    path('api/all-courses/', views.CourseListView.as_view()),

  # Offers endpoints
    path('api/offers/', views.OfferListCreateView.as_view(), name='offer-list'),
    path('api/offers/<int:pk>/', views.OfferRetrieveUpdateDeleteView.as_view(), name='offer-detail'),


 # Purchases / Checkout
    path('api/purchases/', views.PurchaseListView.as_view()),
    path('api/checkout/', views.checkout, name='checkout'),
     path('login/', views.login_view),
    path('checkout/', views.checkout),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)