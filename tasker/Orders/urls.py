from djangos.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    path('insert_order/', views.insert_order),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
