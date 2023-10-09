import random
import matplotlib.pyplot as plt

# Define the dimensions of the square
square_size = 10  # Change this to adjust the size of the square

# Define a list of possible segment lengths
segment_lengths = [1.0, 4.0, 7.0]  # Adjust the lengths as needed

# Function to generate a random line segment within the square with a specified length and orientation
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

# Number of random line segments to generate
num_segments = 20  # Change this to the desired number of line segments

# Generate random line segments with varying lengths and orientations
line_segments = [generate_random_line_segment(segment_lengths) for _ in range(num_segments)]

# Plot the square
plt.figure(figsize=(6, 6))
plt.plot([0, square_size, square_size, 0, 0], [0, 0, square_size, square_size, 0], 'b-')

# Plot the random line segments
for segment in line_segments:
    x1, y1, x2, y2 = segment
    plt.plot([x1, x2], [y1, y2], 'r-')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Random Line Segments in a Square with Varying Lengths and Orientations')
plt.xlim(0, square_size)
plt.ylim(0, square_size)
plt.grid(True)
plt.show()

