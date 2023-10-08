import random
import matplotlib.pyplot as plt

# Define the dimensions of the square
square_size = 10  # Change this to adjust the size of the square

# Function to generate random parallel line segments within the square
def generate_random_parallel_segments():
    horizontal = random.choice([True, False])  # Randomly choose horizontal or vertical
    if horizontal:
        y = random.uniform(0, square_size)
        x1 = random.uniform(0, square_size)
        x2 = random.uniform(0, square_size)
        return (x1, y, x2, y)
    else:
        x = random.uniform(0, square_size)
        y1 = random.uniform(0, square_size)
        y2 = random.uniform(0, square_size)
        return (x, y1, x, y2)

# Number of random parallel line segments to generate
num_segments = 10  # Change this to the desired number of line segments

# Generate random parallel line segments
line_segments = [generate_random_parallel_segments() for _ in range(num_segments)]

# Plot the square
plt.figure(figsize=(6, 6))
plt.plot([0, square_size, square_size, 0, 0], [0, 0, square_size, square_size, 0], 'b-')

# Plot the random parallel line segments
for segment in line_segments:
    x1, y1, x2, y2 = segment
    plt.plot([x1, x2], [y1, y2], 'r-')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Random Parallel Line Segments in a Square')
plt.xlim(0, square_size)
plt.ylim(0, square_size)
plt.grid(True)
plt.show()
