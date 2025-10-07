# routes/utils.py
from collections import defaultdict
import heapq
from .models import Airport, AirportRoute
from django.db.models import Prefetch

def find_nth_node(start_code: str, direction: str, n: int):
    """
    Move 'n' steps in 'direction' from start_code.
    n=1 returns the immediate child.
    Returns Airport instance or None if path breaks early.
    """
    try:
        current = Airport.objects.get(code=start_code)
    except Airport.DoesNotExist:
        return None

    for _ in range(n):
        try:
            route = AirportRoute.objects.get(from_airport=current, position=direction)
            current = route.to_airport
        except AirportRoute.DoesNotExist:
            return None
    return current

def find_longest_node(start_code: str):
    """
    From start airport, pick the outgoing route with the maximum duration.
    Returns Airport (child) or None.
    """
    try:
        airport = Airport.objects.get(code=start_code)
    except Airport.DoesNotExist:
        return None
    route = AirportRoute.objects.filter(from_airport=airport).order_by('-duration').first()
    return route.to_airport if route else None

def find_shortest_route_between(from_code: str, to_code: str):
    """
    Multi-hop shortest path (Dijkstra) on directed graph with weights = duration.
    Returns dict: {'distance': int, 'path': [airport_codes], 'routes': [AirportRoute,...]} or None.
    """
    try:
        start = Airport.objects.get(code=from_code)
        target = Airport.objects.get(code=to_code)
    except Airport.DoesNotExist:
        return None

    # Build adjacency list
    # Preload routes to avoid N+1 queries
    all_routes = AirportRoute.objects.select_related('from_airport', 'to_airport').all()
    graph = defaultdict(list)
    route_map = {}  # (from_id,to_id) -> route
    for r in all_routes:
        graph[r.from_airport_id].append((r.to_airport_id, r.duration))
        route_map[(r.from_airport_id, r.to_airport_id)] = r

    # Dijkstra
    dist = {start.id: 0}
    prev = {}
    heap = [(0, start.id)]

    while heap:
        d, node = heapq.heappop(heap)
        if d != dist.get(node, float('inf')):
            continue
        if node == target.id:
            break
        for neighbor, weight in graph.get(node, []):
            nd = d + weight
            if nd < dist.get(neighbor, float('inf')):
                dist[neighbor] = nd
                prev[neighbor] = node
                heapq.heappush(heap, (nd, neighbor))

    if target.id not in dist:
        return None  # no path

    # reconstruct path
    path_ids = []
    cur = target.id
    while cur != start.id:
        path_ids.append(cur)
        cur = prev[cur]
    path_ids.append(start.id)
    path_ids.reverse()

    # map ids to codes and route objects
    airports = Airport.objects.in_bulk(path_ids)
    path_codes = [airports[_id].code for _id in path_ids]

    routes = []
    for a, b in zip(path_ids, path_ids[1:]):
        routes.append(route_map.get((a, b)))

    return {
        'distance': dist[target.id],
        'path': path_codes,
        'routes': routes
    }
