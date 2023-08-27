import time, random, statistics
import matplotlib.pyplot as plt

# Constant variables (weights are in grams)

# Target weight in grams (female bullmastiff)
GOAL = 50_000

# Total number of adult rats your lab can support
NUM_RATS = 10

# Minimum weight of adult rat, in grams, in initial population
INITIAL_MIN_WT = 200
# Maximum weight of adult rat, in grams, in initial population
INITIAL_MAX_WT = 600
# Most common adult rat weight, in grams, in initial population
INITIAL_MODE_WT = 300

# Probability of a mutation occurring in a rat
MUTATE_ODDS = 0.01
# Scalar on rat weight of least beneficial mutation
MUTATE_MIN = 0.5
# Scalar on rat weight of most beneficial mutation
MUTATE_MAX = 1.2

# Number of pups per pair of mating rats
LITTER_SIZE = 8
# Number of litters per year per pair of matingrats
LITTERS_PER_YEAR = 10
# Generational cutoff to stop breeding program
GENERATION_LIMIT = 500

# check for even user input of rats
def check_rat_input(num_rats):
    if num_rats % 2 != 0:
        num_rats += 1

# Initialize a population with triangular distribution of weights
def populate(num_rats, min_wt, max_wt, mode_wt):
    return [int(random.triangular(min_wt, max_wt, mode_wt)) for i in range(num_rats)] 

# Measure population fitness based on an attribute mean vs target
def fitness(population, goal):
    average = statistics.mean(population)

    return average / goal

# Cull a population to retain only a specified number of members
def select(population, to_retain):
    sorted_popualtion = sorted(population)
    to_retain_by_sex = to_retain//2
    members_per_sex = len(sorted_popualtion)//2

    females = sorted_popualtion[:members_per_sex]
    males = sorted_popualtion[members_per_sex:]

    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]

    return selected_males, selected_females

# Crossover genes among members(weights) of a population
def breed(males, females, litter_size):
    random.shuffle(males)
    random.shuffle(females)

    children = []

    for male, female in zip(males, females):
        for child in range(litter_size):
            child = random.randint(female, male)
            children.append(child)
    
    return children

# Randomly alter rat weights using input odds and fractional changes
def mutate(children, mutate_odss, mutate_min, mutate_max):
    for index, rat in enumerate(children):
        if mutate_odss >= random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))

    return children

# Initialize population, select, breed, and mutate, display results
def main():

    global generations
    generations = 0
    global average_wt
    average_wt = []

    parents = populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT)

    print("initial population weights = {}".format(parents))
    popl_fitness = fitness(parents, GOAL) 

    print("initial population fitness = {}".format(popl_fitness))    
    print("number to retain = {}".format(NUM_RATS))

    while popl_fitness < 1 and generations < GENERATION_LIMIT:
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)

        parents = selected_males + selected_females + children
        popl_fitness = fitness(parents, GOAL)

        #print("Generation {} fitness = {:.4f}".format(generations, popl_fitness))

        average_wt.append(int(statistics.mean(parents)))
        generations += 1

    #print("average weight per generation = {}".format(average_wt))
    print("\nnumber of generations = {}".format(generations))
    print("number of years = {}".format(generations / LITTERS_PER_YEAR))


if __name__ == "__main__":
    start_time = time.time()
    
    check_rat_input(NUM_RATS)
    main()

    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {:.3f} seconds.".format(duration))

    # Create subplots (1 row, 3 columns)
    # Three subplots for different number of rats the lab can support: 10, 20, 50
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 3, 1)
    plt.scatter(range(len(average_wt)), average_wt, label="Max Rats: " + str(NUM_RATS), color='r', marker='o', s=1)
    plt.xlabel('Generations')
    plt.ylabel('Average Weight')
    # display number of years needed to hit 50,000 g rats. If max generation limit is before then, display >50 years
    plt.title("Subplot 1 ({}) Years".format(generations / LITTERS_PER_YEAR if (generations / LITTERS_PER_YEAR) < 50 else ">50"))
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.ylim(1, 50_000)
    plt.xlim(1, 500)

    NUM_RATS = 20
    # rerun main for new data
    main()

    # subplot 2
    plt.subplot(1, 3, 2)
    plt.scatter(range(len(average_wt)), average_wt, label="Max Rats: " + str(NUM_RATS), color='b', marker='o', s=1)
    plt.xlabel('Generations')
    plt.ylabel('Average Weight')
    plt.title("Subplot 2 ({}) Years".format(str(generations / LITTERS_PER_YEAR)))
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.xlim(1, 500)

    NUM_RATS = 50
    # rerun main for new data  
    main()

    # subplot 3
    plt.subplot(1, 3, 3)
    plt.scatter(range(len(average_wt)), average_wt, label="Max Rats: " + str(NUM_RATS), color='g', marker='o', s=1)
    plt.xlabel('Generations')
    plt.ylabel('Average Weight')
    plt.title("Subplot 3 ({}) Years".format(str(generations / LITTERS_PER_YEAR)))
    plt.grid(True)
    plt.legend(loc='lower right')
    plt.xlim(1, 500)

    plt.tight_layout()
    plt.show()

