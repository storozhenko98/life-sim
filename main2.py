import random


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(height)] for _ in range(width)]

    def place_organism(self, organism, x, y):
        self.grid[x][y] = organism
        organism.x = x
        organism.y = y

    def remove_organism(self, x, y):
        self.grid[x][y] = None

    def get_organism(self, x, y):
        return self.grid[x][y]


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
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x = (organism.x + dx) % grid.width
        new_y = (organism.y + dy) % grid.height
        if grid.get_organism(new_x, new_y) is None:
            return new_x, new_y
    return organism.x, organism.y


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
        print(f"Step {step + 1}")
        print_grid(grid, organisms)
        updated_organisms = []

        resources = [(generate_random_coordinates(grid), generate_resource()) for _ in range(10)]

        for organism in organisms:
            organism.strength -= 1
            if organism.strength <= 0:
                grid.remove_organism(organism.x, organism.y)
                continue

            new_x, new_y = move_organism(organism, grid)
            other_organism = grid.get_organism(new_x, new_y)
            if other_organism is not None:
                interaction_type, winner = interact(organism, other_organism, generate_resource())
                print(f"Interaction happened: {interaction_type}")
                if interaction_type == "fight":
                    print(f"Winner: {winner.family}")
                if winner is organism:
                    updated_organisms.append(organism)
                elif winner is other_organism:
                    updated_organisms.append(other_organism)
            else:
                for resource_x, resource_y in [coord for coord, value in resources]:
                    if new_x == resource_x and new_y == resource_y:
                        resource = next(value for coord, value in resources if coord == (resource_x, resource_y))
                        organism.consume(resource)
                        break
                grid.remove_organism(organism.x, organism.y)
                grid.place_organism(organism, new_x, new_y)
                updated_organisms.append(organism)

        organisms = [organism for organism in updated_organisms if organism.strength > 0]

grid = Grid(5, 5)
organisms = place_initial_organisms(grid)
run_simulation(grid, organisms, 30)
