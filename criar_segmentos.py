import random
from collections import namedtuple
import matplotlib.pyplot as plt

# Define a Point namedtuple to represent a point in 2D space
Point = namedtuple('Point', ['x', 'y'])

# Define a namedtuple to represent a line segment with left and right endpoints
Segment = namedtuple('Segment', ['left', 'right'])

# Define an Event namedtuple to represent an event in the sweep line algorithm
Event = namedtuple('Event', ['x', 'y', 'isLeft', 'index'])

# Define the dimensions of the square
square_size = 10  # Change this to adjust the size of the square

# Function to generate a random line segment within the square with a specified length
def generate_random_line_segment(segment_length):
    x1 = random.uniform(0, square_size - segment_length)
    y1 = random.uniform(0, square_size - segment_length)
    x2 = x1 + segment_length
    y2 = y1 if random.choice([True, False]) else y1 + segment_length
    return (x1, y1, x2, y2)

    # x2 = x1 + segment_length
    # y2 = y1 if random.choice([True, False]) else y1 + segment_length
    # left = Point(x1, y1)
    # right = Point(x2, y2)
    # return Segment(left, right)

# Number of random line segments to generate
num_segments = 20  # Change this to the desired number of line segments

# Specify the desired segment length (change as needed)
segment_length = 2


# Generate random line segments with the specified length
line_segments = [generate_random_line_segment(segment_length) for _ in range(num_segments)]

# Plot the square
plt.figure(figsize=(6, 6))
plt.plot([0, square_size, square_size, 0, 0], [0, 0, square_size, square_size, 0], 'b-')

# Plot the random line segments

# Plot the random line segments
for segment in line_segments:
    x1, y1, x2, y2 = segment
    plt.plot([x1, x2], [y1, y2], 'r-', label='Line Segment')
    
# for segment in line_segments:
#     x1 = segment.left.x
#     y1 = segment.left.y
#     x2 = segment.right.x
#     y2 = segment.right.y
#     plt.plot([x1, x2], [y1, y2], 'r-')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title(f'Random Line Segments in a Square (Length = {segment_length})')
plt.xlim(0, square_size)
plt.ylim(0, square_size)
plt.grid(True)
plt.show()
