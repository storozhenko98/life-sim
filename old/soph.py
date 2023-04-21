import random
from collections import defaultdict

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
    def interact_with(self, other, resource_value):
        interaction = None

        if self.family == other.family:
            interaction = "cooperate"
        else:
            # Calculate the gain from cooperation
            cooperation_gain = resource_value // 2

            # Calculate the gain from fighting
            fight_gain = self.calculate_fight_gain(other, resource_value)

            if cooperation_gain > fight_gain:
                interaction = "cooperate"
            else:
                interaction = "fight"

        if interaction == "cooperate":
            print(f"Interaction happened between {self.family} and {other.family}: cooperation")
            return {"interaction": interaction}
        elif interaction == "fight":
            winner = self if self.strength > other.strength else other
            print(f"Interaction happened between {self.family} and {other.family}: fight")
            print(f"Organism {winner.family} won the fight")
            return {"interaction": interaction, "winner": winner}

    def calculate_fight_gain(self, other, resource_value):
        return resource_value if self.strength > other.strength else 0

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

def interact(organism1, organism2, resource_value):
    interaction_result = organism1.interact_with(organism2, resource_value)
    interaction = interaction_result["interaction"]

    if interaction == "cooperate":
        organism1.consume(resource_value // 2)
        organism2.consume(resource_value // 2)
    elif interaction == "fight":
        winner = interaction_result["winner"]
        winner.consume(resource_value)

    return interaction, winner if interaction == "fight" else None
10

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

def run_simulation(grid, organisms, steps, den):
    interactions = {"fight": 0, "cooperate": 0}
    family_stats = defaultdict(lambda: {"last_step": 0, "fights": 0, "cooperations": 0})
    
    for step in range(steps):
        if len(organisms) >= grid.width * grid.height:
            print("\nThe grid is full. Stopping the simulation.")
            break
        print(f"\nStep {step + 1}")
        print_grid(grid, organisms)
        updated_organisms = []

        resources = []
        while len(resources) < den:
            resource_x, resource_y = generate_random_coordinates(grid)
            resource_value = generate_resource()
            if (resource_x, resource_y) not in [coord for coord, value in resources]:
                resources.append(((resource_x, resource_y), resource_value))

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
                interactions[interaction_type] += 1
                family_stats[organism.family].setdefault(interaction_type, 0)
                family_stats[organism.family][interaction_type] += 1
                family_stats[other_organism.family].setdefault(interaction_type, 0)
                family_stats[other_organism.family][interaction_type] += 1


                if interaction_type == "fight":
                    print(f"Winner: {winner.family}")
                    if winner is organism:
                        grid.remove_organism(new_x, new_y)
                    else:
                        grid.remove_organism(old_x, old_y)
                else:
                    grid.remove_organism(old_x, old_y)

            offspring = organism.reproduce()
            if offspring is not None:
                offspring_x, offspring_y = generate_random_coordinates(grid)
                while grid.get_organism(offspring_x, offspring_y) is not None:
                    offspring_x, offspring_y = generate_random_coordinates(grid)
                grid.place_organism(offspring, offspring_x, offspring_y)
                updated_organisms.append(offspring)
                print(f"Organism {organism.family} reproduced at ({offspring_x}, {offspring_y})")

            if organism.strength > 0:
                grid.remove_organism(old_x, old_y)
                grid.place_organism(organism, new_x, new_y)
                updated_organisms.append(organism)

            for resource_x, resource_y in [coord for coord, value in resources]:
                if new_x == resource_x and new_y == resource_y:
                    resource = next(value for coord, value in resources if coord == (resource_x, resource_y))
                    organism.consume(resource)
                    print(f"Organism {organism.family} consumed resource {resource} at ({resource_x}, {resource_y})")

        organisms = [organism for organism in updated_organisms if organism.strength > 0]

        for organism in organisms:
            family_stats[organism.family]["last_step"] = step + 1

    # Find the family with the longest survival time
    longest_surviving_family = max(family_stats, key=lambda f: family_stats[f]["last_step"])
    family_data = family_stats[longest_surviving_family]

    print("\nSimulation statistics:")
    print(f"Family that lasted the longest: {longest_surviving_family}")
    print(f"Steps survived: {family_data['last_step']}")
    print(f"Times fought: {family_data['fights']}")
    print(f"Times cooperated: {family_data['cooperations']}")

Gx = int(input("Grid X size [number only]: "))
Gy = int(input("Grid Y size [number only]: "))
Rounds = int(input("Enter number of simulation steps [number only]: "))
RDensityP = int(input("Enter resource density 0-100 [number only]: "))
Rden = round((Gx * Gy) * (RDensityP / 100))
print(Gx, Gy, Rounds, Rden)
grid = Grid(Gx, Gy)
organisms = place_initial_organisms(grid)
run_simulation(grid, organisms, Rounds, Rden)
