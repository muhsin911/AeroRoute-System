from django.urls import path
from . import views

app_name = 'routes'

urlpatterns = [
    path('', views.home, name='home'),
    path('add-route/', views.add_route, name='add_route'),
    path('nth-node/', views.nth_node, name='nth_node'),
    path('longest-node/', views.longest_node, name='longest_node'),
    path('shortest-node/', views.shortest_node, name='shortest_node'),
]
