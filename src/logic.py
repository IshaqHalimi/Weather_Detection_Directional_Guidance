# ishaq halimi
# CMPSC 463 Project 2
# Weather Detection & Directional Guidance # core graph + Dijkstra for
# December 3rd, 2025

import heapq
import random

NODE_LABELS = {
    1: "Sutherland Building",
    2: "Lot G & F",
    3: "Lot J & H",
    4: "Athletic Building",
    5: "Tennis Courts / Athletic Field",
    6: "Lares Building",
    7: "Woodland Building",
    8: "Spring House",
    9: "Rydal Building",
}

# Weighted roads (bidirectional) blueprint
# Each tuple is (u, v, time_minutes).
EDGES = [
    (3, 1, 4),
    (3, 2, 3),
    (3, 4, 5),

    (2, 4, 4),
    (2, 1, 3),

    (4, 5, 2),
    (4, 9, 8),

    (5, 7, 4),
    (5, 6, 3),

    (6, 8, 3),
    (1, 6, 2),

    (8, 7, 2),
    (7, 9, 6),
]

# Build adjacency list
def edge_key(u, v):
    return tuple(sorted((u, v)))

ADJ = {i: [] for i in range(1, 10)}  # nodes 1..9

for u, v, w in EDGES:
    ADJ[u].append((v, w))
    ADJ[v].append((u, w))


# Weather events: randomly block roads (edges)
EVENT_TYPES = ["TORNADO", "FLOODING", "DEBRIS"]


# Randomly picks a weather event and block some edges.

# Returns:   event_name (str), blocked_edges (set[(u,v)])

def run_randomizer(start=None, end=None):

    all_edges = [edge_key(u, v) for (u, v, _) in EDGES]
    blocked_edges = set()
    event = random.choice(EVENT_TYPES)

    random.shuffle(all_edges)

    if event == "TORNADO":
        # block up to 2 roads
        for ek in all_edges[:2]:
            blocked_edges.add(ek)
    elif event == "FLOODING":
        # block 1–2 roads
        for ek in all_edges[:2]:
            blocked_edges.add(ek)
    else:  # DEBRIS
        # block up to 3 roads
        for ek in all_edges[:3]:
            blocked_edges.add(ek)

    # don't only kill the direct start-end edge if others are blocked
    if start is not None and end is not None:
        direct = edge_key(start, end)
        if direct in blocked_edges and len(blocked_edges) > 1:
            blocked_edges.remove(direct)

    return event, blocked_edges


# Dijkstra on campus graph
def dijkstra(start, goal, blocked_edges):

    INF = float("inf")
    dist = {n: INF for n in ADJ}
    prev = {n: None for n in ADJ}

    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == goal:
            break

        for v, w in ADJ[u]:
            if edge_key(u, v) in blocked_edges:
                continue
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if dist[goal] == INF:
        return [], INF

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path, dist[goal]
