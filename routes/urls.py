from django.urls import path
from . import views

app_name = 'routes'

# Define the URL patterns for this app, linking paths to views
urlpatterns = [
    # Root URL - Homepage of the routes app
    path('', views.home, name='home'),

    # URL path for adding a new route - shows a form and processes submissions
    path('add-route/', views.add_route, name='add_route'),

    # URL path for searching the Nth left or right node in a route network
    path('nth-node/', views.nth_node, name='nth_node'),

    # URL path for finding the longest direct route from an airport
    path('longest-node/', views.longest_node, name='longest_node'),

    # URL path for finding the shortest multi-hop route between two airports
    path('shortest-node/', views.shortest_node, name='shortest_node'),
]
