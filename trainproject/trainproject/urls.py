"""trainproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from trainticketapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home_view),
    path('book/', views.book_view),
    path('print_booked_tickets/', views.print_booked_tickets),
    path('delete/<int:id>/', views.delete_view),
    path('print_available_tickets/', views.print_available_tickets),
    path('select_rac_seats/', views.rac_seats),
    path('waiting_list/', views.waiting_list),
    path('print_booked_rac_tickets/', views.print_booked_RAC_tickets),
    path('alloted_waiting_list/', views.alloted_waiting_list),
]
