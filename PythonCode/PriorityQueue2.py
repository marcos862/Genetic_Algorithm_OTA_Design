#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mibolano
#
# Created:     13/11/2018
# Copyright:   (c) mibolano 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Queue as Q

class Skill():
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print ("New Level: ", description)
        return

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)


def main():
    q = Q.PriorityQueue()
    q.put(Skill(5, 'Proficient'))
    q.put(Skill(10, 'Expert'))
    q.put(Skill(1, 'Novice'))

    while not q.empty():
        next_level = q.get()
        print ('Processing level:', next_level.description)


if __name__ == '__main__':
    main()
