import random
import matplotlib.pyplot as plt
from sortedcontainers import SortedDict

# Define the dimensions of the square
square_size = 10  # Change this to adjust the size of the square

# Function to generate a random line segment within the square with a specified length
def generate_random_line_segment(segment_length):
    x1 = random.uniform(0, square_size - segment_length)
    y1 = random.uniform(0, square_size - segment_length)
    x2 = x1 + segment_length
    y2 = y1 if random.choice([True, False]) else y1 + segment_length
    return ((x1, y1), (x2, y2))  # Return a tuple of two points

# Function to check if two line segments intersect
def do_segments_intersect(segment1, segment2):
    ((x1, y1), (x2, y2)) = segment1  # Unpack points from the first segment
    ((x3, y3), (x4, y4)) = segment2  # Unpack points from the second segment

    # Check if the segments intersect using a simplified approach
    if min(x1, x2) <= max(x3, x4) and min(x3, x4) <= max(x1, x2) and min(y1, y2) <= max(y3, y4) and min(y3, y4) <= max(y1, y2):
        return True

    return False

# Number of random line segments to generate
num_segments = 20  # Change this to the desired number of line segments

# Specify the desired segment length (change as needed)
segment_length = 2

# Generate random line segments with the specified length
line_segments = [generate_random_line_segment(segment_length) for _ in range(num_segments)]

# Check for intersections among the generated line segments
intersections = SortedDict()  # Use a SortedDict to store intersections

for i in range(len(line_segments)):
    for j in range(i + 1, len(line_segments)):
        if do_segments_intersect(line_segments[i], line_segments[j]):
            intersections[(i, j)] = (line_segments[i], line_segments[j])

# Count the number of intersections
intersection_count = len(intersections)

# Print the intersections (you can replace this with any desired action)
print("Intersections:")
for key, intersection in intersections.items():
    print(key, intersection)

# Print the intersection count
print("Intersection Count:", intersection_count)

# Plot the square and random line segments
plt.figure(figsize=(6, 6))
plt.plot([0, square_size, square_size, 0, 0], [0, 0, square_size, square_size, 0], 'b-')

for segment in line_segments:
    (x1, y1), (x2, y2) = segment  # Unpack points from the segment
    plt.plot([x1, x2], [y1, y2], 'r-')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title(f'Random Line Segments in a Square (Length = {segment_length})')
plt.xlim(0, square_size)
plt.ylim(0, square_size)
plt.grid(True)
plt.legend()
plt.show()

