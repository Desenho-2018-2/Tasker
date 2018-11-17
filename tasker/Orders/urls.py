from djangos.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Orders.views.observer import OrderObserver

urlpatterns = [
    path('register_observer/', OrderObserver.as_view()m name='register_observer'),
]
