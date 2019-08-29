# coding: utf-8

import random
import logging
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

class MontyHall:
    __num          = 3
    __choice       = -1
    __false_choice = -1

    def __init__(self, num = 3):
        self.__num    = num
        assert(self.__num > 0)
        self.award    = [False] * 3
        self.award[0] = True
        random.shuffle(self.award)
        self.door     = [False] * 3
        logging.info("Monty Hall problem initialized with length[%d]." % (self.__num))

    def __str__(self):
        return "awards: %s\tdoors: %s\tchoice: %d [%s]" % \
                (str(self.award), str(self.door), self.__choice, self.award[self.__choice])

    def choose_door(self):
        while True:
            choice = random.randint(0, self.__num - 1)
            if choice != self.__choice and not self.door[choice]:
                self.__choice = choice
                break
        logging.info("Participator chooses [%d]." % (self.__choice))
        return None

    def open_false_door(self):
        while True:
            false_choice = random.randint(0, self.__num - 1)
            if false_choice != self.__choice and \
                not self.door[false_choice] and \
                not self.award[false_choice]:
                self.__false_choice = false_choice
                self.door[self.__false_choice] = True
                break
        logging.info("Game manager eliminates a wrong answer [%d]." % (self.__false_choice))
        return None

    def check_chosen_door(self):
        self.door[self.__choice] = True
        logging.warn("The choice of the participator is [%s]." % (self.award[self.__choice]))
        logging.info("%s" % (str(self)))
        return self.award[self.__choice]

def test_monty_hall(num = 3):
    mh = MontyHall(num)
    mh.choose_door()
    mh.open_false_door()
    return mh.check_chosen_door()

def test_monty_hall_with_change(num = 3):
    mh = MontyHall(num)
    mh.choose_door()
    mh.open_false_door()
    mh.choose_door()
    return mh.check_chosen_door()

def report_monty_hall_test(test_func, num = 3, test_num = 1000):
    true_count = 0
    for i in range(test_num):
        if test_func():
            true_count += 1
    return float(true_count) / test_num

def plot_results(results, name = ""):
    round_num = len(results)

    y_mean = np.mean(results)
    y_std  = np.std(results)
    x      = range(0, round_num)
    y      = results

    pl1 = plt.figure(figsize=(8,4))
    plt.title("The frequency of the success in each round")
    plt.xlabel("round")
    plt.ylabel("frequency")
    tx = round_num / 2
    ty = y_mean
    label_var  = r"$\sigma (X)=$%f" % (y_std)
    label_mean = "$X=$%f" % y_mean
    p1_label   = "%s and %s" % (label_var, label_mean)
    p1 = plt.plot(x, y, "-", color = 'orange', label = p1_label, linewidth = 2)
    plt.legend(loc = 'upper left')
    plt.savefig("%s_frequency.png" % (name))
    plt.close()

    plt.title("The distribution plot of the frequency of the success")
    plt.xlabel("$x$")
    plt.ylabel("$f(x)$")
    p2 = plt.hist(results, 40, color = 'orange', normed = 1, alpha = 0.8)
    plt.savefig("%s_distrubution.png" % (name))
    plt.close()

if __name__ == "__main__":
    logging.basicConfig(format = "%(levelname)s: %(message)s", level = logging.ERROR)
    num       = 3
    test_num  = 1000
    round_num = 10000

    unchange_results   = list()
    notice = "\runchange round completed %.2f%%: %s"
    for i in range(round_num):
        precent = float(i) / round_num
        bar = "=" * int(precent * 80) + ">"
        bar = bar + ' ' * (81 - len(bar)) + "| 100%"
        print (notice % (precent * 100, bar)),
        unchange_results.append(report_monty_hall_test(test_monty_hall, num, test_num))
    print(notice % (100, "=" * 80 + ">" + "| 100%"))
    plot_results(unchange_results, "unchange")

    change_results    = list()
    notice = "\rchange round completed %.2f%%:   %s"
    for i in range(round_num):
        precent = float(i) / round_num
        bar = "=" * int(precent * 80) + ">"
        bar = bar + ' ' * (81 - len(bar)) + "| 100%"
        print (notice % (precent * 100, bar)),
        change_results.append(report_monty_hall_test(test_monty_hall_with_change, num, test_num))
    print(notice % (100, "=" * 80 + ">" + "| 100%"))
    plot_results(change_results,   "change")

