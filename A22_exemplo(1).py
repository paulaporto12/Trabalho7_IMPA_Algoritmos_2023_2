from sortedcontainers import SortedList
import random
import heapq
import matplotlib.pyplot as plt



def generate_random_line_segment(segment_length, num_segments):
    segments = []
    for _ in range(num_segments):
        x1 = random.uniform(0, square_size - segment_length)
        y1 = random.uniform(0, square_size - segment_length)
        x2 = x1 + segment_length
        y2 = y1 if random.choice([True, False]) else y1 + segment_length
        segments.append(((x1, y1), (x2, y2)))  # Fix the append here
    return segments


def do_segments_intersect(segment1, segment2):
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]

    def orientation(P, Q, R):
        val = (Q[0] - P[0]) * (R[1] - P[1]) - (R[0] - P[0]) * (Q[1] - P[1])
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    Orientation1 = orientation((x1, y1), (x2, y2), (x3, y3))
    Orientation2 = orientation((x1, y1), (x2, y2), (x4, y4))
    Orientation3 = orientation((x3, y3), (x4, y4), (x1, y1))
    Orientation4 = orientation((x3, y3), (x4, y4), (x2, y2))

    if Orientation1 != Orientation2 and Orientation3 != Orientation4:
        return True

    # Special cases for collinear segments
    if (
        (Orientation1 == 0 and is_on_segment((x1, y1), (x3, y3), (x2, y2)))
        or (Orientation2 == 0 and is_on_segment((x1, y1), (x4, y4), (x2, y2)))
        or (Orientation3 == 0 and is_on_segment((x3, y3), (x1, y1), (x4, y4)))
        or (Orientation4 == 0 and is_on_segment((x3, y3), (x2, y2), (x4, y4)))
    ):
        return True

    return False


def is_on_segment(P, Q, R):
    return (
        Q[0] <= max(P[0], R[0])
        and Q[0] >= min(P[0], R[0])
        and Q[1] <= max(P[1], R[1])
        and Q[1] >= min(P[1], R[1])
    )


square_size = 10

class AVLNode:
    def __init__(self, key, event, left=None, right=None):
        self.key = key
        self.event = event
        self.left = left
        self.right = right
        self.height = 1

def get_height(node):
    if node is None:
        return 0
    return node.height

def update_height(node):
    if node is not None:
        node.height = max(get_height(node.left), get_height(node.right)) + 1

def get_balance_factor(node):
    if node is None:
        return 0
    return get_height(node.left) - get_height(node.right)

def rotate_left(node):
    right_child = node.right
    node.right = right_child.left
    right_child.left = node

    update_height(node)
    update_height(right_child)

    return right_child

def rotate_right(node):
    left_child = node.left
    node.left = left_child.right
    left_child.right = node

    update_height(node)
    update_height(left_child)

    return left_child

def insert_avl(root, key, value):
    if root is None:
        return AVLNode(key, value)

    if key < root.key:
        root.left = insert_avl(root.left, key, value)
    else:
        root.right = insert_avl(root.right, key, value)

    update_height(root)
    balance = get_balance_factor(root)

    if balance > 1:
        if key < root.left.key:
            return rotate_right(root)
        else:
            root.left = rotate_left(root.left)
            return rotate_right(root)

    if balance < -1:
        if key > root.right.key:
            return rotate_left(root)
        else:
            root.right = rotate_right(root.right)
            return rotate_left(root)

    return root

def delete_min_avl(root):
    if root is None:
        return None

    if root.left is None:
        return root.right

    root.left = delete_min_avl(root.left)
    update_height(root)
    balance = get_balance_factor(root)

    if balance > 1:
        if get_balance_factor(root.left) >= 0:
            return rotate_right(root)
        else:
            root.left = rotate_left(root.left)
            return rotate_right(root)

    return root


events_tree = None
class Event:
    def __init__(self, x, segment, event_type):
        self.x = x
        self.segment = segment
        self.event_type = event_type

    def __lt__(self, other):
        return self.x < other.x

def find_segment_intersections(segments):
    events = None  

    for i, segment in enumerate(segments):
        start, end = segment
        event_start = Event(start[0], i, "start")
        event_end = Event(end[0], i, "end")
        events = insert_avl(events, event_start, event_start)
        events = insert_avl(events, event_end, event_end)

    active_segments = SortedList()
    while events:
        min_event = events
        while min_event.left is not None:
            min_event = min_event.left

        x, segment_idx, event_type = min_event.event.x, min_event.event.segment, min_event.event.event_type

        if event_type == "start":
            active_segments.add(segment_idx)
            segment = segments[segment_idx]
            pred = active_segments.bisect_left(segment_idx)
            succ = pred + 1

            if pred > 0 and do_segments_intersect(segments[active_segments[pred - 1]], segment):
                print(f"Segments {segment_idx} and {active_segments[pred - 1]} intersect.")
            if succ < len(active_segments) and do_segments_intersect(segments[active_segments[succ]], segment):
                print(f"Segments {segment_idx} and {active_segments[succ]} intersect.")
        
        elif event_type == "end":
            segment = segments[segment_idx]
            pred = active_segments.bisect_left(segment_idx)
            succ = pred + 1
            print()
            print(f"succ: {succ} --- pred: {pred} --- present: {segment_idx}")
            if (
                0 < pred < len(active_segments)
                and do_segments_intersect(
                    segments[active_segments[pred]], segment
                )  # troca de pred-1 -> pred
                and succ < len(active_segments)
                and do_segments_intersect(segments[active_segments[succ]], segment)
            ):
                print(
                    f"Segments {active_segments[pred]} and {active_segments[succ]} intersect."
                )
            active_segments.remove(segment_idx)
        
        events = delete_min_avl(events)  # Remove the processed event from the AVL tree


num_segments = 100
segment_length = 4
random_segments = generate_random_line_segment(segment_length, num_segments)

find_segment_intersections(random_segments)
