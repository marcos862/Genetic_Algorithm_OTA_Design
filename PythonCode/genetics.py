import matplotlib.pyplot as plt
import copy
import random as r
import Queue as Q

JustAnalyze = False

class Individual():
    def __init__(self, createArray, fn, Genotype_Length):
        self.fn = fn
        self.x1 = 0.0
        self.x2 = 0.0
        self.fitness = 0
        self.Genotype_Length = Genotype_Length
        self.Max_Value = (10**(self.Genotype_Length / 2) - 1) * 1.0
        self.expectedValue = 0
        if createArray:
            self.genotype = [0]*Genotype_Length

    def clone(self):
        ind = Individual(False, self.fn, self.Genotype_Length)
        ind.x1 = self.x1
        ind.x2 = self.x2
        ind.genotype = copy.deepcopy(self.genotype)
        return ind

    def updatePhenotype(self):
        x1 = 0.0
        x2 = 0.0
        for i in xrange(self.Genotype_Length / 2):
            x1 += (self.genotype[i] * 10**i) * 1.0
            x2 += (self.genotype[i + self.Genotype_Length / 2] * 10**i) * 1.0
        self.x1 = self.fn.getRangeX1()[0] + (x1 / self.Max_Value) * (self.fn.getRangeX1()[1] - self.fn.getRangeX1()[0])
        self.x2 = self.fn.getRangeX2()[0] + (x2 / self.Max_Value) * (self.fn.getRangeX2()[1] - self.fn.getRangeX2()[0])

    def updateFitness(self):
        self.fitness = self.fn.getFitness(self.fn.evaluate(self.x1, self.x2))

    def initRandom(self):
        for i in xrange(self.Genotype_Length):
            self.genotype[i] = int(r.random() * 10)
        self.updatePhenotype()

    def __cmp__(self, ind):
        return cmp(ind.fitness, self.fitness)

class GeneticsAlgorithms():
    def __init__(self, fn, Generations, Genotype_Length, Crossover_Odds = 0.8, Mutation_Odds = 0.2):
        self.fn = fn
        self.Generations = Generations
        self.Genotype_Length = Genotype_Length
        #self.Population_Size = 10 * Genotype_Length
        self.Population_Size = 100
        self.Crossover_Odds = Crossover_Odds
        self.Mutation_Odds = Mutation_Odds
        self.population = []
        self.Max_Value = 10**(self.Genotype_Length / 2) - 1
        self.bestIndividual = 0

    def _createPopulation(self):
        for i in xrange(self.Population_Size):
            self.population.append(Individual(True, self.fn, self.Genotype_Length))
            self.population[i].initRandom()

    def _calculateFitness(self):
        previousBestIndividual = self.bestIndividual
        for i in xrange(self.Population_Size):
            self.population[i].updatePhenotype();
            self.population[i].updateFitness()
            if(self.population[i].fitness > self.population[self.bestIndividual].fitness):
                self.bestIndividual = i
        if(previousBestIndividual != self.bestIndividual):
            print "--> BestIndividual found: {}".format(self.population[self.bestIndividual].fitness)

    def _rouletteSelection(self):
        MIN = 0.9
        MAX = 1.1
        queue = Q.PriorityQueue()
        tmpPopulation = []
        for i in xrange(self.Population_Size):
            queue.put(self.population[i])
        for i in xrange(self.Population_Size):
            ind = queue.get()
            ind.expectedValue = MIN + (MAX - MIN) * (i + 1) / self.Population_Size

        for i in xrange(self.Population_Size):
            if i == self.bestIndividual:
                tmpPopulation.append(self.population[i].clone())
                continue
            rnd = self.Population_Size * r.random()
            sum = 0
            j = 0
            while sum < rnd and j < self.Population_Size:
                sum += self.population[i].expectedValue
                j += 1
            tmpPopulation.append(self.population[j - 1].clone())
        self.population = copy.deepcopy(tmpPopulation)

    def _crossover(self):
        for i in range(0, self.Population_Size, 2):
            if (i == self.bestIndividual) or (i + 1 == self.bestIndividual):
                continue
            if r.random() > self.Crossover_Odds:
                continue
            gen1 = self.population[i].genotype
            gen2 = self.population[i + 1].genotype
            i1 = int(r.random() * self.Genotype_Length)
            i2 = int(r.random() * self.Genotype_Length)
            if i2 < i1:
                i1, i2 = i2, i1
            for j in range(i1, i2 + 1, 1):
                if r.random() < 0.5:
                    gen1[j], gen2[j] = gen2[j], gen1[j]

    def _mutation(self):
        for i in xrange(self.Population_Size):
            if (i == self.bestIndividual):
                continue
            if r.random() > self.Mutation_Odds:
                continue
            i1 = int(r.random() * self.Genotype_Length)
            gen1 = self.population[i].genotype
            t = gen1[i1]
            b = int(r.random() * 10)
            while(b == t): b = int(r.random() * 10)
            gen1[i1] = b

    def Run(self):
        self._createPopulation()
        for i in xrange(self.Generations):
            print("Generation: {}".format(i))
            self._calculateFitness()
            self._rouletteSelection()
            self._crossover()
            self._mutation()
        self._calculateFitness()
        bestInd = self.population[self.bestIndividual]
        print("Best: f({}, {}) = {}, fitness = {}\n".format(bestInd.x1, bestInd.x2, bestInd.fn.evaluate(bestInd.x1, bestInd.x2), bestInd.fitness))
        return bestInd


def getBWandGainFromLogFiles(path2LogFiles, BW, Gain):
    import OTA2Evaluate as fn
    import os

    bw_array = []
    gain_array = []
    fitness_array = []
    count = 0
    f = fn.OTA_Basic(BW, Gain)
    if not os.path.lexists(path2LogFiles):
        raise Exception("#######   The Path2LogFiles Doesn't Exist  !!!!!! #######")
    #dirname = os.path.dirname(path2LogFiles)
    filename = os.path.basename(fn.path2baseCircuit)
    filename = filename.replace('.net', '_0.net')
    fullpath = os.path.join(path2LogFiles, filename)
    while os.path.lexists(fullpath):
        bw, gain = f._getBWandGain(fullpath, rmv_files = False)
        bw_array.append(bw)
        gain_array.append(gain)
        fitness_array.append(f.getFitness([bw, gain]))
        count = count + 1
        filename = filename.replace('_{}.net'.format(count - 1), '_{}.net'.format(count))
        fullpath = os.path.join(path2LogFiles, filename)

    return bw_array, gain_array, fitness_array

def plot_Statitistics(bw_array, gain_array, fitness_array, Population_Size, Generations):
    plt.figure(1)
    plt.title('Statistics')
    plt.subplot(311)
    plt.plot(bw_array)
    plt.ylabel('Bandwidth')
    plt.xlabel('Iterations')

    for i in range(1, Generations + 1):
        plt.plot([Population_Size * i, Population_Size * i], [min(bw_array), max(bw_array)], 'k-')

    plt.subplot(312)
    plt.plot(gain_array)
    plt.ylabel('Gain')
    plt.xlabel('Iterationts')
    for i in range(1, Generations + 1):
        plt.plot([Population_Size * i, Population_Size * i], [min(gain_array), max(gain_array)], 'k-')

    plt.subplot(313)
    plt.plot(fitness_array)
    plt.ylabel('Fitness')
    plt.xlabel('Iterationts')
    for i in range(1, Generations + 1):
        plt.plot([Population_Size * i, Population_Size * i], [min(fitness_array), max(fitness_array)], 'k-')
    plt.show()

def main():
    import OTA2Evaluate as fn
    #fn.path2baseCircuit = r'C:\Users\marco\Documents\ProyectoFinal\Circuit\OTA_Basic.net'

    BW = 50e6
    Gain = 80 # This is in DB
    Generations = 50
    GenotypeLength = 12*2
    Population_Size = 100

    if JustAnalyze:
        bw_array, gain_array, fitness_array = getBWandGainFromLogFiles(fn.path2TempCircuits, BW, Gain)  # This is used when we want
    else:
        f = fn.OTA_Basic(BW, Gain)
        gn = GeneticsAlgorithms(f, Generations, GenotypeLength)
        gn.Population_Size = Population_Size
        gn.Run()

        bw_array = fn.BW_array
        gain_array = fn.Gain_array
        fitness_array = fn.Fitness_array

    plot_Statitistics(bw_array, gain_array, fitness_array, Population_Size, Generations)


if __name__ == '__main__':
    main()
