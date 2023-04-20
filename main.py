import random

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[None for _ in range(width)] for _ in range(height)]

    def place_organism(self, organism, x, y):
        self.cells[y][x] = organism
        organism.x = x
        organism.y = y

    def get_organism(self, x, y):
        return self.cells[y][x]

    def remove_organism(self, x, y):
        self.cells[y][x] = None

class Organism:
    def __init__(self, family_id, strength=5):
        self.family_id = family_id
        self.strength = strength
        self.x = None
        self.y = None

    def reproduce(self):
        new_organism = Organism(self.family_id, strength=4)
        return new_organism

    def consume(self, resource):
        self.strength += resource.value
        if self.strength > 10:
            self.strength = 10

    def __str__(self):
        return f"{self.family_id}{self.strength}"

class Resource:
    def __init__(self, value):
        self.value = value

def generate_random_coordinates(grid):
    x = random.randint(0, grid.width - 1)
    y = random.randint(0, grid.height - 1)
    return x, y

def place_initial_organisms(grid):
    organisms = [Organism(family_id=chr(ord('a') + i)) for i in range(5)]
    for organism in organisms:
        x, y = generate_random_coordinates(grid)
        while grid.get_organism(x, y) is not None:
            x, y = generate_random_coordinates(grid)
        grid.place_organism(organism, x, y)
    return organisms

def generate_resource():
    value = random.randint(1, 10)
    return Resource(value)

def move_organism(organism, grid):
    dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
    new_x = (organism.x + dx) % grid.width
    new_y = (organism.y + dy) % grid.height
    return new_x, new_y

def interact(organism1, organism2, resource):
    if random.random() < 0.5:  # cooperation
        organism1.consume(Resource(resource.value // 2))
        organism2.consume(Resource(resource.value // 2))
        return None
    else:  # fight
        total_strength = organism1.strength + organism2.strength
        win_probability1 = organism1.strength / total_strength
        winner = organism1 if random.random() < win_probability1 else organism2
        winner.consume(resource)
        return winner

def print_grid(grid, organisms):
    for y in range(grid.height):
        for x in range(grid.width):
            organism = grid.get_organism(x, y)
            if organism is not None:
                print(str(organism), end=" ")
            else:
                print("--", end=" ")
        print()
def is_grid_full(grid):
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.get_organism(x, y) is None:
                return False
    return True

def run_simulation(grid, organisms, steps):
    for step in range(steps):
        print(f"Step {step + 1}")
        print_grid(grid, organisms)
        updated_organisms = []
        for organism in organisms:
            new_x, new_y = move_organism(organism, grid)
            other_organism = grid.get_organism(new_x, new_y)
            if other_organism is not None:
                resource = generate_resource()
                winner = interact(organism, other_organism, resource)
                if winner is organism:
                    updated_organisms.append(organism)
                if winner is other_organism:
                    updated_organisms.append(other_organism)
            else:
                resource = generate_resource()
                organism.consume(resource)
                grid.remove_organism(organism.x, organism.y)
                grid.place_organism(organism, new_x, new_y)
                updated_organisms.append(organism)

            if organism.strength >= 8 and not is_grid_full(grid):
                new_organism = organism.reproduce()
                updated_organisms.append(new_organism)
                x, y = generate_random_coordinates(grid)
                while grid.get_organism(x, y) is not None:
                    x, y = generate_random_coordinates(grid)
                grid.place_organism(new_organism, x, y)

        organisms = updated_organisms

grid = Grid(10, 10)
organisms = place_initial_organisms(grid)
run_simulation(grid, organisms, 100)
