import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
black    = (  0,   0,   0)
white    = (255, 255, 255)

class Shape:
    def __init__(self):
        self.blocks = []
        self.x = 100
        self.y = -10

class Grid:
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.grid = [[0]*self.cols for _ in range(self.rows)]

def clear_lines(grid):
    lines_to_clear = []
    for i in range(grid.rows):
        if all(block != 0 for block in grid.grid[i]):
            lines_to_clear.append(i)
    for line in reversed(lines_to_clear):
        del grid.grid[line]
        grid.grid.insert(line, [0]*grid.cols)

    return len(lines_to_clear)

clock = pygame.time.Clock()

shapes = [
    Shape(),
    Shape(),
    Shape(),
    Shape(),
    Shape(),
    Shape(),
    Shape()
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen = pygame.display.set_mode((400, 600))
    
    shape_type = random.choice(shapes)
    
    grid = Grid()
    lines_cleared = 0
    
    # Ensure y and x coordinates are within grid boundaries before trying to access them.
    if int(shape_type.y/20) < grid.rows and int(shape_type.x/20) < grid.cols:
        for block in shape_type.blocks:
            for x, value in enumerate(block):
                row = int((shape_type.y + 10)/20)
                col = int((shape_type.x + x)/20)
                
                # Check if the block collides with an existing one
                if grid.grid[row][col] != 0:
                    shape_type.y -= 1
                    break

        for i in range(grid.rows):
            for j in range(grid.cols):
                if grid.grid[i][j] == 1:
                    pygame.draw.rect(screen, white, [j * 20, i * 20 + shape_type.y, 20, 20])

        # Draw shapes on the screen
        for block in shape_type.blocks:
            for x, value in enumerate(block):
                if value == 1:
                    pygame.draw.rect(screen, white, [(int(shape_type.x/20) + x)*20, (int(shape_type.y/20))*20 + shape_type.y, 20, 20])

        lines_cleared = clear_lines(grid)
        
        shape_type.y += 1
        
    if lines_cleared > 0:
        grid.grid.insert(0,[1]*grid.cols)
        for i in range(lines_cleared):
            grid.grid[i] = [0]*grid.cols
        running = True

    pygame.time.Clock().tick(60)

pygame.quit()