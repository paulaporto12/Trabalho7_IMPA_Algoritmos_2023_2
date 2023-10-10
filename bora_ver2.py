import random
import matplotlib.pyplot as plt
import pickle
import time
import tqdm

# Define the dimensions of the square
square_size = 100  # Change this to adjust the size of the square


# Function to generate a random line segment within the square with a specified length
def generate_random_line_segment(segment_lengths):
    segment_length = random.choice(segment_lengths)
    x1 = random.uniform(0, square_size - segment_length)
    y1 = random.uniform(0, square_size - segment_length)
    
    # Randomly choose the orientation (horizontal or vertical)
    if random.choice([True, False]):
        x2 = x1 + segment_length
        y2 = y1
    else:
        x2 = x1
        y2 = y1 + segment_length
    
    return (x1, y1, x2, y2)

# Function to check if two line segments intersect
def do_segments_intersect(segment1, segment2):
    x1, y1, x2, y2 = segment1
    x3, y3, x4, y4 = segment2

    def orientation(P, Q, R):
        val = (Q[0] - P[0]) * (R[1] - P[1]) - (R[0] - P[0]) * (Q[1] - P[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else -1  # Clockwise or Counterclockwise

    Orientation1 = orientation((x1, y1), (x2, y2), (x3, y3))
    Orientation2 = orientation((x1, y1), (x2, y2), (x4, y4))
    Orientation3 = orientation((x3, y3), (x4, y4), (x1, y1))
    Orientation4 = orientation((x3, y3), (x4, y4), (x2, y2))

    if Orientation1 != Orientation2 and Orientation3 != Orientation4:
        return True  # Segments intersect

    # Special cases for collinear segments
    if (
        (Orientation1 == 0 and is_on_segment((x1, y1), (x3, y3), (x2, y2)))
        or (Orientation2 == 0 and is_on_segment((x1, y1), (x4, y4), (x2, y2)))
        or (Orientation3 == 0 and is_on_segment((x3, y3), (x1, y1), (x4, y4)))
        or (Orientation4 == 0 and is_on_segment((x3, y3), (x2, y2), (x4, y4)))
    ):
        return True  # Segments are collinear and overlap

    return False  # Segments do not intersect


def is_on_segment(P, Q, R):
    # Check if point Q lies on line segment PR
    return (
        Q[0] <= max(P[0], R[0])
        and Q[0] >= min(P[0], R[0])
        and Q[1] <= max(P[1], R[1])
        and Q[1] >= min(P[1], R[1])
    )


# Bentley-Ottmann algorithm for line segment intersection detection
def find_intersections(segments):
    events = []
    for segment in segments:
        x1, y1, x2, y2 = segment
        events.append((x1, "start", segment))
        events.append((x2, "end", segment))
    events.sort()

    active_segments = []

    intersections = []

    for event in events:
        x, event_type, segment = event
        if event_type == "start":
            for active_segment in active_segments:
                if do_segments_intersect(active_segment, segment):
                    intersections.append((active_segment, segment))
            active_segments.append(segment)
        else:
            active_segments.remove(segment)

    return intersections


if __name__ == "__main__":
    # Number of random line segments to generate

    # Specify the desired segment length (change as needed)
    segment_length = [2.0, 10.0, 25.0]

    #Generate random line segments with the specified length
    m = 3  # n° de experimentos pra cada valor, pra tirar média
    num_segments = 10000  # valor máximo de segmentos
    l = []
    t = []
    for n in tqdm.tqdm(range(1, num_segments, 100)):
        line_segments = [
            generate_random_line_segment(segment_length) for _ in range(n)
        ]

        start = time.time()
        _ = [find_intersections(line_segments) for _ in range(m)]
        end = time.time()
        dur = end - start

        l.append(n)
        t.append(dur / m)

    with open("experiment_1.pkl", "wb") as file:
        pickle.dump((t, l), file)  # salvando medidas em arquivo

    ##PARA CARREGAR O ARQUIVO POSTERIORMENTE:
    # with open("experiment_1.pkl", "rb") as file:
    #     t, l = pickle.load(file)      # agora só usar t, l no matplotlib

    # intersection_count = len(intersections)

    # print(f"Number of intersections: {intersection_count}")

    # Plot the square and random line segments
    # plt.figure(figsize=(6, 6))
    # plt.plot(
    #     [0, square_size, square_size, 0, 0], [0, 0, square_size, square_size, 0], "b-"
    # )

    # for segment in line_segments:
    #     x1, y1, x2, y2 = segment
    #     plt.plot([x1, x2], [y1, y2], "r-")

    plt.scatter(l, t, s=2)
    plt.show()
    # plt.xlabel("X-axis")
    # plt.ylabel("Y-axis")
    # plt.title(f"Detecção de Segmentos (len = {segment_length})(# = {num_segments})")
    # plt.xlim(0, square_size)
    # plt.ylim(0, square_size)
    # plt.grid(True)
    # plt.legend()
    # plt.show()
