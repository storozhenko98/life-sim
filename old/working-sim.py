import random

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[None for _ in range(height)] for _ in range(width)]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_valid_adjacent_cells(self, x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_cells = []
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self.in_bounds(new_x, new_y):
                valid_cells.append((new_x, new_y))
        return valid_cells

    def place_organism(self, organism, x, y):
        self.cells[x][y] = organism
        organism.x, organism.y = x, y

    def remove_organism(self, x, y):
        self.cells[x][y] = None

    def get_organism(self, x, y):
        return self.cells[x][y]

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
        if self.strength >= 8:
            self.strength = 4
            return Organism(self.family, strength=4)
        return None

def generate_random_coordinates(grid):
    return random.randint(0, grid.width - 1), random.randint(0, grid.height - 1)

def generate_resource():
    return random.randint(1, 10)

def place_initial_organisms(grid):
    families = ["A", "B", "C", "D", "E"]
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
    valid_cells = grid.get_valid_adjacent_cells(organism.x, organism.y)
    new_x, new_y = random.choice(valid_cells)
    return new_x, new_y

def interact(organism1, organism2, resource):
    if organism1.family == organism2.family:
        organism1.consume(resource // 2)
        organism2.consume(resource // 2)
        return "cooperation", None
    else:
        total_strength = organism1.strength + organism2.strength
        probability = organism1.strength / total_strength
        if random.random() < probability:
            organism1.consume(resource)
            return "fight", organism1
        else:
            organism2.consume(resource)
            return "fight", organism2

def print_grid(grid, organisms):
    for y in range(grid.height):
        row = []
        for x in range(grid.width):
            organism = grid.get_organism(x, y)
            if organism is not None:
                row.append(organism.family)
            else:
                row.append(".")
        print(" ".join(row))
    print("")

def run_simulation(grid, organisms, steps, Den):
    for step in range(steps):
        print(f"\nStep {step + 1}")
        print_grid(grid, organisms)
        updated_organisms = []

        resources = [(generate_random_coordinates(grid), generate_resource()) for _ in range(Den)]

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
Gx = int(input("Grid X size [number only]: "))
Gy = int(input("Grid Y size [number only]: "))
Rounds = int(input("Enter number of simulation steps [number only]: "))
RDensityP = int(input("Enter resource density 0-100 [number only]: "))
Rden = round((Gx * Gy) * (RDensityP / 100))
print(Gx, Gy, Rounds, Rden)
grid = Grid(Gx, Gy)
organisms = place_initial_organisms(grid)
run_simulation(grid, organisms, Rounds, Rden)
