import random
import matplotlib.pyplot as plt

# Define the dimensions of the square
square_size = 10  # Change this to adjust the size of the square

# Define a Node structure for the binary search tree
class Node:
    def __init__(self, intersection):
        self.intersection = intersection
        self.left = None
        self.right = None

# Function to insert an intersection into the BST
def insert(root, intersection):
    if root is None:
        return Node(intersection)
    
    # Compare intersections based on some criteria (e.g., x-coordinate)
    if intersection_compare(intersection, root.intersection) < 0:
        root.left = insert(root.left, intersection)
    else:
        root.right = insert(root.right, intersection)

    return root

# Function to perform an in-order traversal of the BST
def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.intersection)
        inorder_traversal(root.right)

# Function to compare two intersections based on x-coordinate
def intersection_compare(intersection1, intersection2):
    x1, y1 = intersection1[0][0], intersection1[0][1]
    x2, y2 = intersection2[0][0], intersection2[0][1]
    if x1 < x2:
        return -1
    elif x1 > x2:
        return 1
    else:
        if y1 < y2:
            return -1
        elif y1 > y2:
            return 1
        else:
            return 0

# Function to generate a random line segment within the square with a specified length
def generate_random_line_segment(segment_length):
    x1 = random.uniform(0, square_size - segment_length)
    y1 = random.uniform(0, square_size - segment_length)
    x2 = x1 + segment_length
    y2 = y1 if random.choice([True, False]) else y1 + segment_length
    return ((x1, y1), (x2, y2))  # Return a tuple of two points

# Function to check if two line segments intersect
def do_segments_intersect(segment1, segment2):
    (x1, y1), (x2, y2) = segment1  # Unpack points from the first segment
    (x3, y3), (x4, y4) = segment2  # Unpack points from the second segment

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
    if (Orientation1 == 0 and is_on_segment((x1, y1), (x3, y3), (x2, y2))) or \
       (Orientation2 == 0 and is_on_segment((x1, y1), (x4, y4), (x2, y2))) or \
       (Orientation3 == 0 and is_on_segment((x3, y3), (x1, y1), (x4, y4))) or \
       (Orientation4 == 0 and is_on_segment((x3, y3), (x2, y2), (x4, y4))):
        return True  # Segments are collinear and overlap

    return False  # Segments do not intersect

def is_on_segment(P, Q, R):
    # Check if point Q lies on line segment PR
    return (Q[0] <= max(P[0], R[0]) and Q[0] >= min(P[0], R[0]) and
            Q[1] <= max(P[1], R[1]) and Q[1] >= min(P[1], R[1]))

# Number of random line segments to generate
num_segments = 20  # Change this to the desired number of line segments

# Specify the desired segment length (change as needed)
segment_length = 2

# Generate random line segments with the specified length
line_segments = [generate_random_line_segment(segment_length) for _ in range(num_segments)]

# Initialize the root of the BST
bst_root = None

# Check for intersections among the generated line segments
for i in range(len(line_segments)):
    for j in range(i + 1, len(line_segments)):
        if do_segments_intersect(line_segments[i], line_segments[j]):
            intersection = (line_segments[i], line_segments[j])
            bst_root = insert(bst_root, intersection)

# Print the intersections using in-order traversal
print("Intersections:")
inorder_traversal(bst_root)

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
