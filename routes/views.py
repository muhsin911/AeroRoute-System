# routes/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AirportRouteForm, NthNodeSearchForm, ShortestNodeSearchForm
from .utils import find_nth_node, find_longest_node, find_shortest_route_between

def home(request):
    return render(request, 'routes/home.html')

def add_route(request):
    if request.method == 'POST':
        form = AirportRouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Route added successfully.")
            return redirect('routes:add_route')
    else:
        form = AirportRouteForm()
    return render(request, 'routes/add_route.html', {'form': form})

def nth_node(request):
    result = None
    if request.method == 'POST':
        form = NthNodeSearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['airport_code']
            direction = form.cleaned_data['direction']
            n = form.cleaned_data['n']
            node = find_nth_node(code, direction, n)
            if node:
                result = f"The {n}th {direction} node from {code} is {node.code} - {node.name}."
            else:
                result = "Node not found (path ended early or airport missing)."
    else:
        form = NthNodeSearchForm()
    return render(request, 'routes/nth_node.html', {'form': form, 'result': result})

def longest_node(request):
    result = None
    if request.method == 'POST':
        code = request.POST.get('airport_code')
        if code:
            node = find_longest_node(code)
            if node:
                result = f"The longest node from {code} is {node.code} - {node.name}."
            else:
                result = "No outgoing routes found or airport missing."
    return render(request, 'routes/longest_node.html', {'result': result})

def shortest_node(request):
    result = None
    form = ShortestNodeSearchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        from_code = form.cleaned_data['from_airport']
        to_code = form.cleaned_data['to_airport']
        res = find_shortest_route_between(from_code, to_code)
        if res:
            result = f"Shortest distance: {res['distance']} km. Path: {' -> '.join(res['path'])}"
        else:
            result = "No path found between the given airports."
    return render(request, 'routes/shortest_node.html', {'form': form, 'result': result})
