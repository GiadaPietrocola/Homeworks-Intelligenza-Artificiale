import heapq
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional


class Node:
    def __init__(self, position: Tuple[int, int], parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Estimated cost from current node to goal
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f


class MuseumEvacuation:
    def __init__(self):
        self.layout = [
            ['0', '0', '1', '0', 'E'],
            ['0', '1', '0', '1', '0'],
            ['P', '0', '0', '0', '0'],
            ['0', '1', '1', '1', '0'],
            ['0', '0', '0', '0', 'E']
        ]
        self.rows = len(self.layout)
        self.cols = len(self.layout[0])

    def find_person_and_exits(self) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        """Find person's position and all emergency exits"""
        person = None
        exits = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.layout[i][j] == 'P':
                    person = (i, j)
                elif self.layout[i][j] == 'E':
                    exits.append((i, j))
        return person, exits

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two points"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            x, y = position[0] + dx, position[1] + dy
            if 0 <= x < self.rows and 0 <= y < self.cols and self.layout[x][y] != '1':
                neighbors.append((x, y))
        return neighbors

    def find_evacuation_path(self) -> Optional[List[Tuple[int, int]]]:
        """Find shortest path to nearest emergency exit"""
        person, exits = self.find_person_and_exits()

        algorithm_steps = []
        frontier = [(0, person)]
        came_from = {person: None}
        cost_so_far = {person: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current in exits:
                algorithm_steps.append(current)
                break

            algorithm_steps.append(current)

            for neighbor in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heuristic=min(self.manhattan_distance(neighbor, exit) for exit in exits)
                    priority = new_cost + heuristic
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        return algorithm_steps

    def display_path(self, path: List[Tuple[int, int]]):
        """Display the evacuation path on the museum layout"""
        for i, j in path:
            if self.layout[i][j] == '0':
                self.layout[i][j] = '.'

    
    def visualize(self, path: List[Tuple[int, int]] = None):
        """
        Visualize the museum layout with matplotlib.
        If path is provided, it will be shown in green.
        """
        # Create figure with smaller size and better cell proportion
        fig, ax = plt.subplots(figsize=(6, 6))

        # Create color map with distinct colors
        cmap = plt.cm.colors.ListedColormap(['#FFFFFF', '#404040', '#FF4444', '#4444FF', '#FFCC00'])

        # Convert layout to numeric array for visualization
        numeric_layout = np.zeros((self.rows, self.cols))
        text_annotations = []  # Store text annotations for cells

        for i in range(self.rows):
            for j in range(self.cols):
                if self.layout[i][j] == '1':  # Wall
                    numeric_layout[i][j] = 1
                    text_annotations.append((i, j, ''))
                elif self.layout[i][j] == 'E':  # Exit
                    numeric_layout[i][j] = 2
                    text_annotations.append((i, j, 'EXIT'))
                elif self.layout[i][j] == 'P':  # Person
                    numeric_layout[i][j] = 3
                    text_annotations.append((i, j, 'P'))
                else:  # Free space
                    text_annotations.append((i, j, ''))

        # Add path if provided
        if path:
            for row, col in path[1:-1]:  # Skip start and end positions
                numeric_layout[row][col] = 4
                text_annotations.append((row, col, '→'))

        # Plot the layout
        im = ax.imshow(numeric_layout, cmap=cmap)

        # Add cell borders
        for i in range(self.rows + 1):
            ax.axhline(i - 0.5, color='black', linewidth=1)
        for j in range(self.cols + 1):
            ax.axvline(j - 0.5, color='black', linewidth=1)

        # Add text annotations
        for i, j, text in text_annotations:
            if text:  # Only add non-empty text
                color = 'white' if numeric_layout[i,j] in [1, 2, 3] else 'black'
                ax.text(j, i, text, ha='center', va='center', color=color,
                       fontweight='bold', fontsize=10)

        # Remove ticks but keep grid lines
        ax.set_xticks([])
        ax.set_yticks([])

        # Add legend with smaller patches
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#FFFFFF', edgecolor='black', label='Free Space'),
            Patch(facecolor='#404040', edgecolor='black', label='Wall'),
            Patch(facecolor='#FF4444', edgecolor='black', label='Exit'),
            Patch(facecolor='#4444FF', edgecolor='black', label='Person'),
        ]
        if path:
            legend_elements.append(Patch(facecolor='#FFCC00', edgecolor='black', label='Path'))

        ax.legend(handles=legend_elements,
                 loc='center left',
                 bbox_to_anchor=(1.05, 0.5),
                 title='Legend',
                 frameon=True,
                 fontsize='small')

        plt.title('Museum Layout', pad=10)
        plt.tight_layout()
        plt.show()