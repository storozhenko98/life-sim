import random


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[None for _ in range(height)] for _ in range(width)]

    def place_organism(self, organism, x, y):
        self.cells[x][y] = organism
        organism.x = x
        organism.y = y

    def remove_organism(self, x, y):
        self.cells[x][y] = None

    def get_organism(self, x, y):
        return self.cells[x][y]

    def is_valid_coordinate(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_valid_adjacent_cells(self, x, y):
        adjacent_cells = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        return [(new_x, new_y) for new_x, new_y in adjacent_cells if self.is_valid_coordinate(new_x, new_y) and self.get_organism(new_x, new_y) is None]


class Organism:
    def __init__(self, family, strength=5):
        self.family = family
        self.strength = strength
        self.x = None
        self.y = None

    def consume(self, resource):
        self.strength += resource
        if self.strength > 10:
            self.strength = 10

    def reproduce(self):
        self.strength //= 2
        return Organism(self.family, strength=self.strength)

    def __str__(self):
        return self.family


def generate_random_coordinates(grid):
    x = random.randint(0, grid.width - 1)
    y = random.randint(0, grid.height - 1)
    return x, y


def place_initial_organisms(grid):
    families = ['a', 'b', 'c', 'd', 'e']
    organisms = []

    for family in families:
        x, y = generate_random_coordinates(grid)
        while grid.get_organism(x, y) is not None:
            x, y = generate_random_coordinates(grid)
        organism = Organism(family)
        grid.place_organism(organism, x, y)
        organisms.append(organism)

    return organisms


def move_organism(organism, grid):
    possible_moves = grid.get_valid_adjacent_cells(organism.x, organism.y)
    new_x, new_y = random.choice(possible_moves)
    return new_x, new_y

def generate_resource():
    return random.randint(1, 10)


def interact(organism1, organism2, resource):
    if organism1.family == organism2.family:
        organism1.consume(resource // 2)
        organism2.consume(resource // 2)
        return "cooperate", None
    else:
        total_strength = organism1.strength + organism2.strength
        if random.random() < organism1.strength / total_strength:
            organism1.consume(resource)
            return "fight", organism1
        else:
            organism2.consume(resource)
            return "fight", organism2


def print_grid(grid, organisms):
    for y in range(grid.height):
        for x in range(grid.width):
            organism = grid.get_organism(x, y)
            if organism is not None:
                print(organism, end=' ')
            else:
                print('.', end=' ')
        print()


def run_simulation(grid, organisms, steps):
    for step in range(steps):
        print(f"\nStep {step + 1}")
        print_grid(grid, organisms)
        updated_organisms = []

        resources = [(generate_random_coordinates(grid), generate_resource()) for _ in range(3)]

        for organism in organisms:
            organism.strength -= 1
            if organism.strength <= 0:
                grid.remove_organism(organism.x, organism.y)
                print(f"Organism {organism.family} died.")
                continue

            old_x, old_y = organism.x, organism.y
            new_x, new_y = move_organism(organism, grid)

            other_organism = grid.get_organism(new_x, new_y)
            if other_organism is not None:
                interaction_type, winner = interact(organism, other_organism, generate_resource())
                print(f"Interaction happened between {organism.family} and {other_organism.family}: {interaction_type}")
                if interaction_type == "fight":
                    print(f"Winner: {winner.family}")
                if winner is organism:
                    grid.remove_organism(old_x, old_y)
                    grid.place_organism(organism, new_x, new_y)
                    updated_organisms.append(organism)
                elif winner is other_organism:
                    updated_organisms.append(other_organism)
            else:
                grid.remove_organism(old_x, old_y)
                grid.place_organism(organism, new_x, new_y)
                updated_organisms.append(organism)

            for resource_x, resource_y in [coord for coord, value in resources]:
                if new_x == resource_x and new_y == resource_y:
                    resource = next(value for coord, value in resources if coord == (resource_x, resource_y))
                    organism.consume(resource)
                    print(f"Organism {organism.family} consumed resource {resource} at ({resource_x}, {resource_y})")

        organisms = [organism for organism in updated_organisms if organism.strength > 0]

grid = Grid(5, 5)
organisms = place_initial_organisms(grid)
run_simulation(grid, organisms, 20)
