import pygame, sys, math, time, heapq

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Route Finding using Beam Search – Rahul Ranjan")
font = pygame.font.SysFont("arial", 20, bold=True)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
BLUE = (60, 130, 250)
GREY = (200, 200, 200)
YELLOW = (250, 230, 90)

# Graph positions (for drawing)
positions = {
    'me': (100, 250),
    'B': (250, 150),
    'C': (250, 350),
    'D': (400, 100),
    'E': (400, 300),
    'F': (550, 350),
    'you': (600, 200)
}

# Graph connections with costs
graph = {
    'me': [('B', 3), ('C', 6)],
    'B': [('D', 4), ('E', 5)],
    'C': [('F', 9)],
    'D': [('you', 7)],
    'E': [('you', 2)],
    'F': [],
    'you': []
}

# Heuristic values
heuristic = {
    'me': 10, 'B': 8, 'C': 9, 'D': 5,
    'E': 3, 'F': 7, 'you': 0
}

# Draw graph nodes and edges
def draw_graph(path=[], explored=set(), start=None, goal=None):
    screen.fill(WHITE)

    # Draw edges
    for node, edges in graph.items():
        for neighbor, cost in edges:
            pygame.draw.line(screen, GREY, positions[node], positions[neighbor], 2)
            midx = (positions[node][0] + positions[neighbor][0]) // 2
            midy = (positions[node][1] + positions[neighbor][1]) // 2
            text = font.render(str(cost), True, BLACK)
            screen.blit(text, (midx, midy))

    # Draw current explored nodes
    for node in explored:
        pygame.draw.circle(screen, RED, positions[node], 25)

    # Draw final path
    if len(path) > 1:
        for i in range(len(path) - 1):
            pygame.draw.line(screen, BLUE, positions[path[i]], positions[path[i + 1]], 4)

    # Draw all nodes
    for node, pos in positions.items():
        if node in path:
            color = GREEN
        elif node == start:
            color = BLUE
        elif node == goal:
            color = RED
        else:
            color = YELLOW

        pygame.draw.circle(screen, color, pos, 25)
        pygame.draw.circle(screen, BLACK, pos, 25, 2)
        label = font.render(node, True, BLACK)
        screen.blit(label, (pos[0] - 8, pos[1] - 10))

    pygame.display.flip()


# Beam Search algorithm (with animation)
def beam_search(start, goal, beam_width):
    queue = [(heuristic[start], [start])]
    explored = set()

    while queue:
        new_paths = []

        # Visualize current queue (exploration)
        for _, path in queue:
            draw_graph(path, explored, start, goal)
            time.sleep(0.6)

        for _, path in queue:
            node = path[-1]
            explored.add(node)
            if node == goal:
                return path

            for neighbor, _ in graph[node]:
                new_path = path + [neighbor]
                h = heuristic[neighbor]
                new_paths.append((h, new_path))

        # Keep only best "beam_width" paths
        queue = heapq.nsmallest(beam_width, new_paths, key=lambda x: x[0])

    return None


# Main game loop
def main():
    start, goal = None, None
    route = []
    beam_width = 2
    running = True

    while running:
        draw_graph(route, start=start, goal=goal)

        # Display info
        info1 = font.render("Click to choose START and GOAL nodes.", True, BLACK)
        info2 = font.render("Press SPACE to run Beam Search | R to reset | ESC to exit", True, BLACK)
        screen.blit(info1, (20, 20))
        screen.blit(info2, (20, 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    start, goal, route = None, None, []
                    pygame.display.set_caption("Route Finding using Beam Search – Rahul Ranjan")
                elif event.key == pygame.K_SPACE and start and goal:
                    pygame.display.set_caption("Running Beam Search...")
                    route = beam_search(start, goal, beam_width)
                    if route:
                        pygame.display.set_caption(f"✅ Route Found: {' → '.join(route)}")
                    else:
                        pygame.display.set_caption("❌ No Route Found")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for node, pos in positions.items():
                    if math.hypot(mx - pos[0], my - pos[1]) < 25:
                        if not start:
                            start = node
                            pygame.display.set_caption(f"Start Node Selected: {start}")
                        elif not goal:
                            goal = node
                            pygame.display.set_caption(f"Goal Node Selected: {goal}")

        clock.tick(30)


# Run the game
if __name__ == "__main__":
    main()
