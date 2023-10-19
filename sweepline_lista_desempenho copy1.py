import heapq
from sortedcontainers import SortedList
import random
import matplotlib.pyplot as plt
import time

square_size = 10


def generate_random_line_segment(segment_length, num_segments):
    segments = []
    for _ in range(num_segments):
        x1 = random.uniform(0, square_size - segment_length)
        y1 = random.uniform(0, square_size - segment_length)
        x2 = x1 + segment_length
        y2 = y1 if random.choice([True, False]) else y1 + segment_length
        segments.append(((x1, y1), (x2, y2)))
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


class Event:
    def __init__(self, x, segment, event_type):
        self.x = x
        self.segment = segment
        self.event_type = event_type

    def __lt__(self, other):
        return (self.x, self.segment, self.event_type) < (
            other.x,
            other.segment,
            other.event_type,
        )


def find_segment_intersections(segments):
    events = []
    num_events_list = []
    num_events_list.append(len(events))  # Record the initial number of events
    status_len = []
    for i, segment in enumerate(segments):
        start, end = segment
        heapq.heappush(events, Event(start[0], i, "start"))
        heapq.heappush(events, Event(end[0], i, "end"))
    active_segments = SortedList()

    num_events_list.append(len(events))  # Record the number of events at this step
    while events:
        event = heapq.heappop(events)
        if event.event_type == "start":
            active_segments.add(event.segment)
            segment = segments[event.segment]
            pred = active_segments.bisect_left(event.segment)
            succ = pred + 1

            if pred > 0 and do_segments_intersect(
                segments[active_segments[pred - 1]], segment
            ):
                print(
                    f"Segments {event.segment} and {active_segments[pred - 1]} intersect."
                )
            if succ < len(active_segments) and do_segments_intersect(
                segments[active_segments[succ]], segment
            ):
                print(
                    f"Segments {event.segment} and {active_segments[succ]} intersect."
                )
        elif event.event_type == "end":
            segment = segments[event.segment]
            pred = active_segments.bisect_left(event.segment)
            succ = pred + 1
            print()
            print(f"succ: {succ} --- pred: {pred} --- present: {event.segment}")
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
            active_segments.remove(event.segment)
        status_len.append(len(active_segments))
        num_events_list.append(len(events))
        # else:
        #     # swap aqui
        #     pass
    return num_events_list, status_len



if __name__ == "__main__":
    num_segments = 2000  # maximum number of segments
    segment_length = 0.5
    num_events_list = []
    status_len = []

    # Call find_segment_intersections to populate num_events_list and status_len
    line_segments = generate_random_line_segment(segment_length, num_segments)
    num_events_list, status_len = find_segment_intersections(line_segments)

    # Create and display the plot for the number of events
    plt.figure(1)
    plt.plot(range(len(num_events_list)), num_events_list)
    plt.xlabel("Step")
    plt.ylabel("Number of Events")
    plt.title("Evolution of the Events List")
    plt.grid()

    # Create and display the plot for the length of the status structure
    plt.figure(2)
    plt.plot(range(len(status_len)), status_len)
    plt.xlabel("Step")
    plt.ylabel("Length of Status Structure")
    plt.title("Evolution of Status Structure Length")
    plt.grid()

    plt.show()
