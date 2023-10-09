import random
import matplotlib.pyplot as plt

# Define the dimensions of the square
square_size = 10  # Change this to adjust the size of the square

# Function to generate random horizontal line segments within the square
def generate_random_horizontal_segments(num_segments, max_length):
    segments = []
    for _ in range(num_segments):
        y = random.uniform(0, square_size)
        x1 = random.uniform(0, square_size - max_length)
        x2 = x1 + random.uniform(0, max_length)
        segments.append((x1, y, x2, y))
    return segments

# Number of random horizontal line segments to generate
num_segments = 10  # Change this to the desired number of line segments
max_segment_length = 3  # Maximum length of line segments

# Generate random horizontal line segments
line_segments = generate_random_horizontal_segments(num_segments, max_segment_length)

# Plot the square
plt.figure(figsize=(6, 6))
plt.plot([0, square_size, square_size, 0, 0], [0, 0, square_size, square_size, 0], 'b-')

# Plot the random horizontal line segments
for segment in line_segments:
    x1, y1, x2, y2 = segment
    plt.plot([x1, x2], [y1, y2], 'r-')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Random Horizontal Line Segments in a Square')
plt.xlim(0, square_size)
plt.ylim(0, square_size)
plt.grid(True)
plt.show()
