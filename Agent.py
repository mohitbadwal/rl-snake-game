"""
    Agent.py created by mohit.badwal
    on 5/1/2018

"""

import _pickle as cPickle
import math
import random
import sys

from data.snake.Environment import SnakeGameEnvironment


class Agent():
    """
  Generic Value-based agent
  """
    Q = {}

    def __init__(self, epsilon, trained_file="", gamma=0.9, alpha=0.8):
        self.gamma = gamma
        self.alpha = alpha
        if epsilon == -1.0:
            self.e = 0.3
        else:
            self.e = epsilon
        self.old_state = None
        self.old_action = None
        self.Q = {}
        self.N = {}
        self.count = 0

        if trained_file is not "":
            try:
                (self.e, self.count, self.Q) = cPickle.load(open(trained_file))
            except IOError as e:
                sys.stderr.write(("File " + trained_file + " not found. \n"))
                sys.exit(1)

        return

    def UpdateQ(self, state, action, state_, action_, reward, explore):
        # raise NotImplemented()
        if not state:
            return

        q = self.Q[state][action]
        if not state_:
            q += self.alpha * (reward - q)
        else:
            q_ = max(self.Q[state_].values())
            q += self.alpha * (reward + self.gamma * q_ - q)

        self.Q[state][action] = q

    def Act(self, state, actions, reward, episode_ended):
        self.count += 1

        # print(actions,rewards)
        if self.count == 10000:
            self.e -= self.e / 20
            self.count = 1000

        # epsilon-greedy
        if state not in self.Q:
            self.Q[state] = {}
            print("New detected")
            for action in actions:
                self.Q[state][action] = 10

        # Explore
        fg = random.random()
        # print(fg , self.e)
        if fg < self.e:
            action = actions[random.randint(0, len(actions) - 1)]
            explore = True
        # Exploit
        else:
            action = max(actions, key=lambda x: self.Q[state][x])
            explore = False
        # i = 0
        # for act in range(len(actions)):
        #     if actions[act] == action:
        #         i = act
        #         break
        # print(reward)
        # print(explore)
        # Update actions
        if episode_ended:
            self.UpdateQ(self.old_state, self.old_action, None, None, reward,
                         explore)
        else:
            self.UpdateQ(self.old_state, self.old_action, state, action, reward,
                         explore)

        self.old_state = state
        self.old_action = action
        return action

    def WriteKnowledge(self, filename):
        fp = open(filename, "w")
        cPickle.dump((self.e, self.count, self.Q), fp)
        fp.close()
        return


if __name__ == '__main__':
    agent = Agent(0.3)

    # A predefined Q dictionary , uncomment to see your snake exploit , set epsilon to any value between -0.05 to -0.9
    # agent.Q = {(0, 0, 0, 1, -1): {'GO_LEFT': -95.79349885590233, 'GO_FORWARD': -97.60108359567943, 'GO_RIGHT': 255.71387320708826}, (0, 0, 0, -1, -1): {'GO_LEFT': 88.14290098266201, 'GO_FORWARD': -98.71713949625001, 'GO_RIGHT': -97.38858203792486}, (0, 0, 0, -1, 1): {'GO_LEFT': -37.33491160428488, 'GO_FORWARD': -96.46499458185764, 'GO_RIGHT': -96.57756192213888}, (0, 0, 0, 1, 1): {'GO_LEFT': -94.4410360731904, 'GO_FORWARD': 51.77057742829655, 'GO_RIGHT': -92.59850377280587}, (0, 0, 0, 1, 0): {'GO_LEFT': -96.340420070923, 'GO_FORWARD': -94.55838542766286, 'GO_RIGHT': 150.31917375405885}, (0, 0, 0, 0, -1): {'GO_LEFT': -99.72618480424737, 'GO_FORWARD': -99.79722084603841, 'GO_RIGHT': 123.98915758887023}, (0, 0, 0, -1, 0): {'GO_LEFT': -95.68129717235972, 'GO_FORWARD': -32.50150499023478, 'GO_RIGHT': -97.18207486665602}, (0, 0, 0, 0, 1): {'GO_LEFT': 9.121010445977447, 'GO_FORWARD': -80.38889375651965, 'GO_RIGHT': -82.87876514641013}, (0, 1, 0, 0, 1): {'GO_LEFT': 220.47034279975514, 'GO_FORWARD': 582.5680180806611, 'GO_RIGHT': 26.141722025211806}, (-1, 0, 0, -1, -1): {'GO_LEFT': -100.0, 'GO_FORWARD': -98.13318391791408, 'GO_RIGHT': 168.33069370793896}, (-1, 0, 0, -1, 1): {'GO_LEFT': -100.0, 'GO_FORWARD': -97.68954558809334, 'GO_RIGHT': 154.41786135718883}, (1, 0, 0, -1, 0): {'GO_LEFT': 474.09619420674693, 'GO_FORWARD': 19.743386301627304, 'GO_RIGHT': -57.60955583340123}, (0, 0, -1, 1, -1): {'GO_LEFT': -9.622569767643753, 'GO_FORWARD': -98.27340756975923, 'GO_RIGHT': -100.0}, (-1, 0, 0, 0, 1): {'GO_LEFT': -100.0, 'GO_FORWARD': -62.23339266919849, 'GO_RIGHT': 108.33804369497196}, (-1, 0, 0, 1, -1): {'GO_LEFT': -100.0, 'GO_FORWARD': -96.02892862540224, 'GO_RIGHT': 32.86715353453597}, (-1, 0, 0, 1, 1): {'GO_LEFT': -100.0, 'GO_FORWARD': 444.0812370725819, 'GO_RIGHT': -95.76362329890304}, (0, 0, 1, 1, 0): {'GO_LEFT': -26.33893333653805, 'GO_FORWARD': 28.824322490800682, 'GO_RIGHT': 907.383790459878}, (0, 0, -1, -1, 1): {'GO_LEFT': 116.05453358079288, 'GO_FORWARD': -96.92162033012659, 'GO_RIGHT': -100.0}, (0, -1, -1, -1, -1): {'GO_LEFT': 74.50524878208441, 'GO_FORWARD': -99.99993739373022, 'GO_RIGHT': -99.99999913542156}, (0, 0, -1, 1, 1): {'GO_LEFT': -98.8824884527099, 'GO_FORWARD': 437.4100006436594, 'GO_RIGHT': -100.0}, (0, -1, 0, -1, -1): {'GO_LEFT': 34.528033560334904, 'GO_FORWARD': -100.0, 'GO_RIGHT': -98.47703746185165}, (-1, 1, 0, 0, 1): {'GO_LEFT': -99.824, 'GO_FORWARD': 633.6518035211157, 'GO_RIGHT': -34.496721889418964}, (-1, 0, -1, 1, 1): {'GO_LEFT': -99.93209706742455, 'GO_FORWARD': 97.55145873567737, 'GO_RIGHT': -99.99988954724118}, (-1, 0, 0, -1, 0): {'GO_LEFT': -99.99999999999864, 'GO_FORWARD': 60.85533276504893, 'GO_RIGHT': -84.66113341034463}, (-1, 0, 0, 1, 0): {'GO_LEFT': -100.0, 'GO_FORWARD': -82.43530625285084, 'GO_RIGHT': 102.57121181773391}, (-1, 0, 0, 0, -1): {'GO_LEFT': -99.73401246159186, 'GO_FORWARD': -18.480080045682328, 'GO_RIGHT': -98.08221792678647}, (0, 1, -1, 0, 1): {'GO_LEFT': 98.31309815728034, 'GO_FORWARD': 577.9528945254024, 'GO_RIGHT': -99.12}, (-1, 0, -1, -1, -1): {'GO_LEFT': -99.99997089888467, 'GO_FORWARD': 87.53239703757285, 'GO_RIGHT': -99.99999994959096}, (0, 0, -1, -1, 0): {'GO_LEFT': -94.80360496606278, 'GO_FORWARD': -57.35117803136515, 'GO_RIGHT': -100.0}, (0, 0, -1, 0, 1): {'GO_LEFT': 282.58538911441855, 'GO_FORWARD': -95.82933725034127, 'GO_RIGHT': -100.0}, (1, 0, -1, -1, 0): {'GO_LEFT': 445.6668242753332, 'GO_FORWARD': -22.082068793490507, 'GO_RIGHT': -99.9997184}, (0, 0, -1, 1, 0): {'GO_LEFT': -96.85372705253242, 'GO_FORWARD': -4.552106571415206, 'GO_RIGHT': -100.0}, (0, -1, -1, 0, 1): {'GO_LEFT': 143.07395239790628, 'GO_FORWARD': -95.6, 'GO_RIGHT': -99.81615195214167}, (0, 0, -1, -1, -1): {'GO_LEFT': 186.53827615725203, 'GO_FORWARD': -98.71528256970495, 'GO_RIGHT': -100.0}, (-1, 0, -1, 1, -1): {'GO_LEFT': -99.99878018790676, 'GO_FORWARD': 136.97441630028504, 'GO_RIGHT': -99.99998440727084}, (-1, -1, -1, -1, -1): {'GO_LEFT': -99.99995694777554, 'GO_FORWARD': -99.99993589300993, 'GO_RIGHT': -99.99993711492854}, (0, -1, 0, 1, 0): {'GO_LEFT': -80.35719202215462, 'GO_FORWARD': -99.9648, 'GO_RIGHT': 52.79557785106391}, (-1, 0, -1, 0, 1): {'GO_LEFT': -99.12, 'GO_FORWARD': 99.06727873762595, 'GO_RIGHT': -97.67921112378323}, (-1, -1, -1, 1, -1): {'GO_LEFT': -99.99513998515961, 'GO_FORWARD': -28.03267722354596, 'GO_RIGHT': -99.9406561103705}, (0, -1, 0, -1, 0): {'GO_LEFT': 20.96385007431857, 'GO_FORWARD': -95.6, 'GO_RIGHT': -90.43294381893784}, (0, -1, 0, 1, -1): {'GO_LEFT': -99.99495770438561, 'GO_FORWARD': -100.0, 'GO_RIGHT': 143.33514085139615}, (0, -1, -1, -1, 1): {'GO_LEFT': -22.18793307313374, 'GO_FORWARD': -99.99452013800959, 'GO_RIGHT': -99.9987638119692}, (0, -1, -1, 1, -1): {'GO_LEFT': 132.26591529699994, 'GO_FORWARD': -99.99999696409193, 'GO_RIGHT': -99.99992022661802}, (0, -1, 0, 0, -1): {'GO_LEFT': -34.991755225523605, 'GO_FORWARD': -99.99296, 'GO_RIGHT': -99.98582553104241}, (0, 0, -1, 0, -1): {'GO_LEFT': -97.50480440435553, 'GO_FORWARD': 143.93750185936844, 'GO_RIGHT': -99.9999977472}, (-1, -1, 0, -1, -1): {'GO_LEFT': -99.99999999958807, 'GO_FORWARD': -99.9999965647089, 'GO_RIGHT': 146.83811254083065}, (-1, -1, 0, 1, -1): {'GO_LEFT': -99.99999695825214, 'GO_FORWARD': -99.99999999999399, 'GO_RIGHT': 3.5128340684206307}, (-1, -1, -1, 0, -1): {'GO_LEFT': -96.60381928380235, 'GO_FORWARD': 10.75222501648335, 'GO_RIGHT': -97.68930257475168}, (0, -1, -1, -1, 0): {'GO_LEFT': 28.00124177226933, 'GO_FORWARD': -99.44173797992418, 'GO_RIGHT': -99.12}, (-1, 0, -1, -1, 1): {'GO_LEFT': -99.85654311293104, 'GO_FORWARD': 25.2976820921459, 'GO_RIGHT': -99.20378055525201}, (-1, 0, -1, 1, 0): {'GO_LEFT': -97.4012182225498, 'GO_FORWARD': 199.03724340023345, 'GO_RIGHT': -99.12}, (-1, -1, 0, -1, 1): {'GO_LEFT': -99.99999954944, 'GO_FORWARD': -99.97461694716073, 'GO_RIGHT': 88.33092132213446}, (-1, 0, 1, 1, 0): {'GO_LEFT': -99.99994368, 'GO_FORWARD': 9.152040154422238, 'GO_RIGHT': 554.9271324706378}, (-1, 0, -1, 0, -1): {'GO_LEFT': -98.59570153870024, 'GO_FORWARD': 265.08117595006655, 'GO_RIGHT': -95.5613185879704}, (0, -1, -1, 1, 1): {'GO_LEFT': 74.13746870310192, 'GO_FORWARD': -99.99984767064171, 'GO_RIGHT': -99.99980799045372}, (0, -1, -1, 1, 0): {'GO_LEFT': 259.6986460007238, 'GO_FORWARD': -99.824, 'GO_RIGHT': -99.12}, (-1, -1, -1, -1, 1): {'GO_LEFT': -99.99999507351693, 'GO_FORWARD': -26.55174056555086, 'GO_RIGHT': -99.99999822572391}, (0, -1, -1, 0, -1): {'GO_LEFT': 140.63664870878782, 'GO_FORWARD': -96.36210747842789, 'GO_RIGHT': -89.90614623846864}, (-1, -1, 0, 0, -1): {'GO_LEFT': -99.10735729259795, 'GO_FORWARD': -97.33878708704725, 'GO_RIGHT': 103.15839011988446}, (1, -1, 0, -1, 0): {'GO_LEFT': 681.52994911739, 'GO_FORWARD': -78.0, 'GO_RIGHT': -24.62535671061377}, (-1, -1, 0, 1, 1): {'GO_LEFT': -98.75742341978082, 'GO_FORWARD': -99.98672932729377, 'GO_RIGHT': 70.49376855065003}, (-1, -1, 0, 1, 0): {'GO_LEFT': -99.99779350410932, 'GO_FORWARD': -99.99296, 'GO_RIGHT': 417.1288958979022}, (-1, 0, -1, -1, 0): {'GO_LEFT': -98.34656155318552, 'GO_FORWARD': 72.96548188957573, 'GO_RIGHT': -95.88458123032973}, (0, -1, 1, 1, 0): {'GO_LEFT': 10, 'GO_FORWARD': 10, 'GO_RIGHT': 999.7659260131727}, (-1, -1, 0, 0, 1): {'GO_LEFT': -95.6, 'GO_FORWARD': -95.6, 'GO_RIGHT': -28.074974439258675}, (-1, -1, -1, 1, 1): {'GO_LEFT': -99.9999999693185, 'GO_FORWARD': -99.82984444655995, 'GO_RIGHT': -99.99999998127217}, (-1, 1, -1, 0, 1): {'GO_LEFT': 10, 'GO_FORWARD': 573.854503847425, 'GO_RIGHT': 10}, (-1, -1, 0, -1, 0): {'GO_LEFT': -99.12, 'GO_FORWARD': -99.12, 'GO_RIGHT': 136.99606830590702}, (1, -1, -1, -1, 0): {'GO_LEFT': 495.69500757881355, 'GO_FORWARD': 10, 'GO_RIGHT': -92.32521418384864}, (-1, -1, 1, 1, 0): {'GO_LEFT': -78.0, 'GO_FORWARD': -78.0, 'GO_RIGHT': 633.078756930744}, (-1, -1, -1, 0, 1): {'GO_LEFT': -99.30037293236157, 'GO_FORWARD': 8.256553845037288, 'GO_RIGHT': -99.35770018595345}, (0, -1, 0, -1, 1): {'GO_LEFT': -96.85422961224458, 'GO_FORWARD': -99.12, 'GO_RIGHT': -62.20766894453493}, (-1, -1, -1, 1, 0): {'GO_LEFT': -99.99974598356079, 'GO_FORWARD': -99.99975055754253, 'GO_RIGHT': -99.32985314795457}, (-1, -1, -1, -1, 0): {'GO_LEFT': -99.99988431064095, 'GO_FORWARD': -99.99953047102615, 'GO_RIGHT': -99.99954036485539}, (0, -1, 0, 1, 1): {'GO_LEFT': -93.85154801412072, 'GO_FORWARD': -99.12, 'GO_RIGHT': -17.86732792707682}, (0, -1, 0, 0, 1): {'GO_LEFT': -38.29265785797585, 'GO_FORWARD': -95.6, 'GO_RIGHT': -83.92651444699251}}


    for i in range(10000):
        game = SnakeGameEnvironment(agent)
        game.setup()
        print(agent.Q)
        # input("hi")
    f = open("temp.pkl", 'wb')
    cPickle.dump(agent.Q, f)
