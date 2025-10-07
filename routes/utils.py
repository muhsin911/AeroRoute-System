from collections import defaultdict
import heapq
from .models import Airport, AirportRoute
from django.db.models import Prefetch


def find_nth_node(start_code: str, direction: str, n: int):
    """
    Traverse 'n' steps in the given 'direction' (left or right) starting from airport with code 'start_code'.
    n=1 returns the immediate child in that direction.
    Returns the Airport instance at the nth position if exists, otherwise None.

    Args:
        start_code: str - Airport code to start from
        direction: str - 'left' or 'right'
        n: int - number of steps to move in the direction

    Returns:
        Airport instance or None if the path breaks before n steps or airport does not exist.
    """
    try:
        # Get starting airport instance by code
        current = Airport.objects.get(code=start_code)
    except Airport.DoesNotExist:
        return None

    # Traverse n times following the given direction link (left or right child)
    for _ in range(n):
        try:
            # Query for the route from current airport in the specified direction
            route = AirportRoute.objects.get(from_airport=current, position=direction)
            # Move to the next airport along the route
            current = route.to_airport
        except AirportRoute.DoesNotExist:
            # If no route exists in direction, return None (path ended early)
            return None
    return current


def find_longest_node(start_code: str):
    """
    Find the outgoing route with the maximum duration from the airport with 'start_code'.
    Returns the Airport instance that is the destination of this longest route.

    Args:
        start_code: str - Airport code to start from

    Returns:
        Airport instance representing the longest child node or None if not found.
    """
    try:
        airport = Airport.objects.get(code=start_code)
    except Airport.DoesNotExist:
        return None

    # Query for the outgoing route with the maximum duration
    route = AirportRoute.objects.filter(from_airport=airport).order_by('-duration').first()

    # Return the destination airport if such a route exists
    return route.to_airport if route else None


def find_shortest_route_between(from_code: str, to_code: str):
    """
    Compute the shortest path between two airports using Dijkstra's algorithm
    over a graph formed by the AirportRoute edges weighted by duration.

    Args:
        from_code: str - Starting airport code
        to_code: str - Target airport code

    Returns:
        dict with keys:
            'distance': total duration of shortest path,
            'path': list of airport codes for the path,
            'routes': list of AirportRoute objects forming the shortest path,
        or None if no path exists.
    """
    try:
        start = Airport.objects.get(code=from_code)
        target = Airport.objects.get(code=to_code)
    except Airport.DoesNotExist:
        return None

    # Build graph adjacency list: node_id -> list of (neighbor_id, weight)
    # Preload all routes with related airports to prevent extra queries (N+1 problem)
    all_routes = AirportRoute.objects.select_related('from_airport', 'to_airport').all()
    graph = defaultdict(list)
    route_map = {}  # Maps (from_id, to_id) tuple to AirportRoute instance

    for r in all_routes:
        graph[r.from_airport_id].append((r.to_airport_id, r.duration))
        route_map[(r.from_airport_id, r.to_airport_id)] = r

    # Initialize Dijkstra algorithm data structures
    dist = {start.id: 0}  # shortest known distance to each node
    prev = {}             # predecessor node in shortest path
    heap = [(0, start.id)]  # min-heap priority queue as (distance, node_id)

    # Main Dijkstra loop
    while heap:
        d, node = heapq.heappop(heap)
        if d != dist.get(node, float('inf')):
            # Skip outdated distance values in heap
            continue
        if node == target.id:
            # Target reached, terminate early
            break
        # Explore neighbors
        for neighbor, weight in graph.get(node, []):
            nd = d + weight
            # Update shortest path if better distance found
            if nd < dist.get(neighbor, float('inf')):
                dist[neighbor] = nd
                prev[neighbor] = node
                heapq.heappush(heap, (nd, neighbor))

    # If target is unreachable, return None
    if target.id not in dist:
        return None

    # Reconstruct the path by walking backward through the predecessors
    path_ids = []
    cur = target.id
    while cur != start.id:
        path_ids.append(cur)
        cur = prev[cur]
    path_ids.append(start.id)
    path_ids.reverse()  # Reverse to get path from start to target

    # Fetch Airport instances from database for path IDs
    airports = Airport.objects.in_bulk(path_ids)

    # Convert path IDs to airport codes for easy readable output
    path_codes = [airports[_id].code for _id in path_ids]

    # Fetch the actual AirportRoute instances for each leg of the path
    routes = []
    for a, b in zip(path_ids, path_ids[1:]):
        routes.append(route_map.get((a, b)))

    # Return comprehensive path and route details
    return {
        'distance': dist[target.id],
        'path': path_codes,
        'routes': routes
    }
