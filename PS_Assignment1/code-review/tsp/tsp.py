import math
import random

class Work():
    def __init__(self, ID, start_node, c):
        self.ID = ID
        self.start_node = start_node
        self.grouping = c
        self.curr_node = self.start_node
        self.graph = self.grouping.graph
        self.path_vec = []
        self.path_vec.append(self.start_node)
        self.pathc = 0
        self.Beta = 1.0
        self.Q0 = 0.5
        self.Rho = 0.99
        self.ntv = {}
        for i in range(0, self.graph.num_nodes):
            if i != self.start_node:
                self.ntv[i] = i
        self.path_mat = []
        for i in range(0, self.graph.num_nodes):
            self.path_mat.append([0] * self.graph.num_nodes)

    #could this be simpler?
    def run(self):
        graph = self.grouping.graph
        while not self.end():
            new_node = self.state_transition_rule(self.curr_node)
            self.pathc += graph.delta(self.curr_node, new_node)
            self.path_vec.append(new_node)
            self.path_mat[self.curr_node][new_node] = 1 
            self.local_updating_rule(self.curr_node, new_node)
            self.curr_node = new_node
        self.pathc += graph.delta(self.path_vec[-1], self.path_vec[0])
        self.grouping.update(self)
        self.__init__(self.ID, self.start_node, self.grouping)

    def end(self):
        return not self.ntv


    def state_transition_rule(self, curr_node):
        graph = self.grouping.graph
        q = random.random()
        max_node = -1
        if q < self.Q0:
            print("Exploitation")
            max_val = -1
            val = None
            for node in list(self.ntv.values()):
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                val = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if val > max_val:
                    max_val = val
                    max_node = node
        else:
            #Bob was here
            print("Exploration")
            sum = 0
            node = -1
            for node in list(self.ntv.values()):
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                sum += graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
            if sum == 0:
                raise Exception("sum = 0")
            avg = sum / len(self.ntv)
            print(("avg = %s" % (avg,)))
            for node in list(self.ntv.values()):
                p = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if p > avg:
                    print(("p = %s" % (p,)))
                    max_node = node
            if max_node == -1:
                max_node = node
        if max_node < 0:
            raise Exception("max_node < 0")
        del self.ntv[max_node]
        return max_node

    def local_updating_rule(self, curr_node, next_node):
        #Update the pheromones on the tau matrix to represent transitions of the ants
        graph = self.grouping.graph
        val = (1 - self.Rho) * graph.tau(curr_node, next_node) + (self.Rho * graph.tau0)
        graph.update_tau(curr_node, next_node, val)


import random
import sys



class BigGroup:
    def __init__(self, graph, num_ants, num_iterations):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Alpha = 0.1
        self.reset()

    def reset(self):
        self.bpc = sys.maxsize
        self.bpv = None
        self.bpm = None
        self.lbpi = 0

    def start(self):
        self.ants = self.c_workers()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()
            # Note that this will help refine the results future iterations.
            self.global_updating_rule()

    def iteration(self):
        self.avg_pathc = 0
        self.ant_counter = 0
        self.iter_counter += 1
        for ant in self.ants:
            ant.run()

    def num_ants(self):
        return len(self.ants)

    def num_iterations(self):
        return self.num_iterations

    def iteration_counter(self):
        return self.iter_counter

    def update(self, ant):
        print(("Update called by %s" % (ant.ID,)))
        self.ant_counter += 1
        self.avg_pathc += ant.pathc
        if ant.pathc < self.bpc:
            self.bpc = ant.pathc
            self.bpm = ant.path_mat
            self.bpv = ant.path_vec
            self.lbpi = self.iter_counter
        if self.ant_counter == len(self.ants):
            self.avg_pathc /= len(self.ants)
            print(("Best: %s, %s, %s, %s" % (
                self.bpv, self.bpc, self.iter_counter, self.avg_pathc,)))


    def done(self):
        return self.iter_counter == self.num_iterations

    def c_workers(self):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = Work(i, random.randint(0, self.graph.num_nodes - 1), self)
            ants.append(ant)

        return ants
   
    def get_phermone_tau(self):
       return self.graph.get_tau()
 
    def global_updating_rule(self):
        #can someone explain this
        evaporation = 0
        deposition = 0
        for r in range(0, self.graph.num_nodes):
            for s in range(0, self.graph.num_nodes):
                if r != s:
                    delt_tau = self.bpm[r][s] / self.bpc
                    evaporation = (1 - self.Alpha) * self.graph.tau(r, s)
                    deposition = self.Alpha * delt_tau
                    self.graph.update_tau(r, s, evaporation + deposition)

class GraphBit:
    def __init__(self, num_nodes, delta_mat, tau_mat=None):
        print((len(delta_mat)))
        if len(delta_mat) != num_nodes:
            raise Exception("len(delta) != num_nodes")
        self.num_nodes = num_nodes
        self.delta_mat = delta_mat 
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, num_nodes):
                self.tau_mat.append([0] * num_nodes)

    def delta(self, r, s):
        return self.delta_mat[r][s]

    def tau(self, r, s):
        return self.tau_mat[r][s]

    def etha(self, r, s):
        return 1.0 / self.delta(r, s)

    def update_tau(self, r, s, val):
        self.tau_mat[r][s] = val

    def get_tau(self):
        return self.tau_mat

    def reset_tau(self):
        avg = self.average_delta()
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)
        print(("Average = %s" % (avg,)))
        print(("Tau0 = %s" % (self.tau0)))
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0


    def average_delta(self):
        sum = 0
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += self.delta_mat[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg


    def average_tau(self):
        sum = 0
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += self.tau_mat[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg


import pickle
import sys
import traceback
import matplotlib.pyplot as plt
import csv

def main(argv):
    nm = 10

    if len(argv) >= 3 and argv[0]:
        nm = int(argv[0])

    if nm <= 10:
        na = 20
        ni = 12
        nr = 4
    else:
        na = 28
        ni = 20
        nr = 4

    stuff = pickle.load(open(argv[1], "r"))
    cities = stuff[0]
    cm = stuff[1]
    #why are we doing this?
    if nm < len(cm):
        cm = cm[0:nm]
        for i in range(0, nm):
            cm[i] = cm[i][0:nm]



    try:
        graph = GraphBit(nm, cm)
        bpv = None
        bpc = sys.maxsize
        for i in range(0, nr):
            print(("Repetition %s" % i))
            graph.reset_tau()
            workers = BigGroup(graph, na, ni)
            print("c Started")
            workers.start()
            if workers.bpc < bpc:
                print("c Path")
                bpv = workers.bpv
                bpc = workers.bpc
        phermones = graph.get_tau()
        print(phermones)
        print("\n------------------------------------------------------------")
        print("                     Results                                ")
        print("------------------------------------------------------------")
        print(("\nBest path = %s" % (bpv,)))
        city_vec = []
        for node in bpv:
            print((cities[node] + " ",))
            city_vec.append(cities[node])
        print(("\nBest path cost = %s\n" % (bpc,)))
        results = [bpv, city_vec, bpc]
        pickle.dump(results, open(argv[2], 'w+'))

    except Exception as e:
        print(("exception: " + str(e)))
        traceback.print_exc()
    
    csvfile = open(argv[3], 'rU')
    csvreader = csv.reader(csvfile)
    citiesd = {}    
    for row in csvreader:
        citiesd[row[0]] = {'lat': float(row[1]), 'lon': float(row[2])}
    csvfile.close()

    plt.figure(figsize=(8,8))
#    plt.xlim(55,58)
#    plt.ylim(-5,-2)
    lats = []
    lons = []
    
    for i in range(0, len(phermones)):
           for y in range(0, len(phermones[i])):
               if i != y:
                   print((citiesd[cities[i]]['lon'], citiesd[cities[i]]['lat'], (citiesd[cities[y]]['lon']-citiesd[cities[i]]['lon']), (citiesd[cities[y]]['lat']-citiesd[cities[i]]['lat'])))
                   plt.arrow(citiesd[cities[i]]['lon'], citiesd[cities[i]]['lat'], (citiesd[cities[y]]['lon']-citiesd[cities[i]]['lon']), (citiesd[cities[y]]['lat']-citiesd[cities[i]]['lat']), length_includes_head=True, alpha=10*phermones[i][y], fc='blue', head_width=None)

    for value in city_vec:
           lats.append(citiesd[value]['lat'])
           lons.append(citiesd[value]['lon'])
    lats.append(citiesd[city_vec[0]]['lat'])
    lons.append(citiesd[city_vec[0]]['lon'])
    print(lats)
    print(lons)
    colors = ['green']+['red'] * (len(lats)-2) + ['green']
    plt.scatter(lons,lats, c=colors,s=25)
    for i in range(0, len(lats) - 1):
        plt.arrow(lons[i], lats[i], (lons[i+1]-lons[i]), (lats[i+1]-lats[i]),length_includes_head = True)
    for label, lats, lons, color in zip(city_vec, lats, lons, colors):
        plt.annotate(
            label, xy = (lons, lats), xytext = (-5, 5),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round', fc = color, alpha = 0.5))
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
