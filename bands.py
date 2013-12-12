import numpy as np
import pygame


class Node:
    def __init__(self, pos = None, prv = None, nxt = None,
                 locked = False, mass = 1.0, jointRigidity = 1.0):
        self.pos = pos          # X, Y, V numpy array
        self.prv = prv          # previous node
        self.nxt = nxt          # next node
        self.locked = locked    # if true, forces have no effect on this node
        self.mass = mass        # 1 / how much a froce effects that node
        self.k = jointRigidity  # coefficient for the tension force

    def calcForces(self):
        totForce = np.array([0, 0, 0])
        totForce = totForce + self.getTensionForce()
        totForce = totForce + self.getObstacleForce()
        return totForce


    def applyForces(self):
        if not self.locked:
            self.pos = self.pos + 1 / self.mass * self.calcForces()
        
    def getTensionForce(self):
        tensionForce = np.array([0, 0, 0])

        if self.prv:
            kPrv = 1 / (1 / self.k + 1 / self.prv.k)
            tensionForce = tensionForce + kPrv * (self.prv.pos - self.pos) / \
                           np.linalg.norm((self.prv.pos - self.pos))

        if self.nxt:
            kNxt = 1 / (1 / self.k + 1 / self.nxt.k)
            tensionForce = tensionForce + kNxt * (self.nxt.pos - self.pos) / \
                           np.linalg.norm((self.nxt.pos - self.pos))

        tensionForce[2] = 0     # We only want a tension force in the XY-plane

        return tensionForce

    def getObstacleForce(self):
        obstacleForce = np.array([0, 0, 0])
        obsPos = np.array([140, 120, 0])
        dist = np.linalg.norm(obsPos - self.pos)

        if dist < 30:
            obstacleForce = (self.pos - obsPos) / (dist*dist)

        return obstacleForce

    def getXY(self):
        return (int(self.pos[0]), int(self.pos[1]))
     
if __name__ == "__main__":

    pygame.init()
    fpsClock = pygame.time.Clock()
    window = pygame.display.set_mode((640, 480))


    head = Node(np.array([90, 90, 0]), None, None, True)
    node = head

    positions = [[131, 131, 0],
                 [180, 80, 0],
                 [380, 20, 0],
                 [20, 20, 0],
                 [50, 20, 0],
                 [120, 100, 0],
                 [100, 50, 0],
                 [180, 300, 0],
                 [250, 190, 0],
                 [500, 300, 0]]

    for pos in positions:
        node.nxt = Node(np.array(pos), node, None)
        node = node.nxt

    node.locked = True

    node = head
    while(node):
        print(node.pos)
        node = node.nxt

    while True:
        window.fill(pygame.Color(0, 0, 0))
        pygame.draw.circle(window, pygame.Color(255, 255, 0), (140, 120), 30, 2)

        node = head
        while(node):
            if node.nxt:
                pygame.draw.line(window, pygame.Color(255, 0, 0), node.getXY(),
                                node.nxt.getXY(), 4)
            pygame.draw.circle(window, pygame.Color(0, 255, 0), node.getXY(),
                               3, 3)

            node.applyForces()
            node = node.nxt

        pygame.display.update()
        fpsClock.tick(100)
