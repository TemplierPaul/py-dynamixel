from multi_quad import MultiQuad
import numpy as np
import py_dynamixel.io as io
import time

class RandomSearch:
    def __init__(self, MQ, popsize = 2, sigma = 0.1, lr=0.5):
        self.MQ = MQ
        self.popsize = popsize
        self.sigma = sigma
        self.lr = lr
        self.center = np.array([0.0]* 16)
        self.population = []
        self.mutation = None

    def evaluate(self):
        self.MQ.multi_traj(self.population)
        self.MQ._exec_traj()

        # Input the index of the best one 
        best = input("Best one? 0/1: ")
        return best
    
    def mutate(self):
        self.population = []
        
        self.mutation = np.random.randn(16) * self.sigma

        self.population = [
            self.center + self.mutation,
            self.center - self.mutation
        ]

    def update(self, best):
        if best == "-1":
            return
        best = int(best)
        # self.center = self.population[best]
        mutation = self.population[best] - self.center
        self.center = self.center + self.lr * mutation

    def run(self, n=5):
        try:
            for gen in range(n):
                print("Generation", gen)
                print(self.center)
                self.mutate()
                print("G1", self.population[0])
                print("G2", self.population[1])
                best = self.evaluate()
                self.update(best)
            # play the final controller

        except KeyboardInterrupt:
            print("KeyboardInterrupt")

        try:
            input("Final controller? ")
            print("Final controller")
            self.MQ.run_new_sin_controller(self.center, duration=10.0)
            self.MQ._exec_traj()
        finally:
            self.MQ.shutdown()



if __name__ == "__main__":
    ports = io.get_available_ports()
    if not ports:
        raise IOError('No port available.')
    
    ctrl_freq = 100
    max_quad = 2

    if max_quad is not None:
        ports = ports[:max_quad]

    MQ = MultiQuad(ports, ctrl_freq)
    MQ.neutral_controller()
    RS = RandomSearch(MQ)
    RS.run(20)
    MQ.shutdown()
