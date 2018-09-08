#!/usr/bin/env python3

# Programming assignment 3: implementing distributed, asynchronous,
#                           distance vector routing.
#
# THIS IS THE MAIN ROUTINE.  IT SHOULD NOT BE TOUCHED AT ALL BY STUDENTS!

import random
import copy
from node0 import rtinit0, rtupdate0, linkhandler0
from node1 import rtinit1, rtupdate1, linkhandler1
from node2 import rtinit2, rtupdate2
from node3 import rtinit3, rtupdate3


LINKCHANGES = 1

TRACE = 1;             # for my debugging
YES = 1;
NO = 0;

# a rtpkt is the packet sent from one routing update process to
# another via the call tolayer3()
class Rtpkt:
    #sourceid       # id of sending router sending this pkt
    #destid         # id of router to which pkt being sent
                   # (must be an immediate neighbor)
    #mincost[4]     # min cost to node 0 ... 3

    def __init__(self, srcid, destid, mincosts):
        self.sourceid = srcid
        self.destid = destid
        self.mincosts = mincosts[:4]


# ***************** NETWORK EMULATION CODE STARTS BELOW ***********
# The code below emulates the layer 2 and below network environment:
#   - emulates the tranmission and delivery (with no loss and no
#     corruption) between two physically connected nodes
#   - calls the initializations routines rtinit0, etc., once before
#     beginning emulation
#
# THERE IS NOT REASON THAT ANY STUDENT SHOULD HAVE TO READ OR UNDERSTAND
# THE CODE BELOW.  YOU SHOLD NOT TOUCH, OR REFERENCE (in your code) ANY
# OF THE DATA STRUCTURES BELOW.  If you're interested in how I designed
# the emulator, you're welcome to look at the code - but again, you should have
# to, and you defeinitely should not have to modify
# ******************************************************************

class Event:
    #evtime           # event time
    #evtype             # event type code
    #eventity           # entity where event occurs

    #rtpkt *rtpktptr # ptr to packet (if any) assoc w/ this event
    def __init__(self, evtime=None, evtype=None, eventity=None, rtpktptr=None):
        self.evtime = evtime
        self.evtype = evtype
        self.eventity = eventity
        self.rtpktptr = rtpktptr

evlist = []   # the event list

# possible events:
FROM_LAYER2 = 2
LINK_CHANGE = 10

clocktime = 0.000


def main():
    init()
    while evlist:
        event = evlist.pop(0)
        if TRACE > 1:
            print("MAIN: rcv event, t=%.3f, at %d" % (event.evtime, event.eventity))
            if event.evtype == FROM_LAYER2:
                print(" src:%2d," % event.rtpktptr.sourceid)
                print(" dest:%2d," % event.rtpktptr.destid)
                print(" contents: %3d %3d %3d %3d\n" %
                      (event.rtpktptr.mincost[0], event.rtpktptr.mincost[1],
                       event.rtpktptr.mincost[2], event.rtpktptr.mincost[3]))
        clocktime = event.evtime;    # update time to next event time

        if event.evtype == FROM_LAYER2:
            if event.eventity == 0:
                rtupdate0(event.rtpktptr)
            elif event.eventity == 1:
                rtupdate1(event.rtpktptr)
            elif event.eventity == 2:
                rtupdate2(event.rtpktptr)
            elif event.eventity == 3:
                rtupdate3(event.rtpktptr)
            else:
                print("Panic: unknown event entity\n")
                exit(0)
        elif event.evtype == LINK_CHANGE:
            if (clocktime<10001.0):
                linkhandler0(1,20)
                linkhandler1(0,20)
            else:
                linkhandler0(1,1)
                linkhandler1(0,1)
        else:
            print("Panic: unknown event type\n")
            exit(0)

        if event.evtype == FROM_LAYER2:
            del event.rtpktptr        # free memory for packet, if any
        del event                     # free memory for event struct


    print("\nSimulator terminated at t=%f, no packets in medium\n" % clocktime);


# initialize the simulator
def init():
    #int i
    #float sum, avg
    #struct event *evptr;

    TRACE = int(input("Enter TRACE:"))

    random.seed(9999)              # init random number generator
    clocktime = 0.0                # initialize time to 0.0
    rtinit0()
    rtinit1()
    rtinit2()
    rtinit3()

    # initialize future link changes
    if LINKCHANGES == 1:
        event = Event(evtime=10000.0,
                      evtype=LINK_CHANGE,
                      eventity=-1,
                      rtpktptr=None)
        insertevent(event)
        event = Event(evtime=20000.0,
                      evtype=LINK_CHANGE,
                      rtpktptr=None)
        insertevent(event)


#********************* EVENT HANDLINE ROUTINES *******
#*  The next set of routines handle the event list   *
#*****************************************************
def insertevent(p):
    # struct event *p;
    # struct event *q,*qold;
    if TRACE > 3:
        print("            INSERTEVENT: time is %lf\n" % clocktime)
        print("            INSERTEVENT: future time will be %lf\n" % p.evtime)

    evlist.append(p)
    evlist.sort(key=lambda e: e.evtime, reverse=True)

def printevlist():
    print("--------------\nEvent List Follows:\n")
    for event in evlist:
        print("Event time: %f, type: %d entity: %d\n" % (event.evtime, event.evtype, event.eventity))
    print("--------------\n")


# ************************** TOLAYER2 ***************
def tolayer2(packet):
    connectcosts = [[0 for j in range(4)] for i in range(4)]

    # initialize by hand since not all compilers allow array initilization
    connectcosts[0][0]=0;  connectcosts[0][1]=1;  connectcosts[0][2]=3;
    connectcosts[0][3]=7;
    connectcosts[1][0]=1;  connectcosts[1][1]=0;  connectcosts[1][2]=1;
    connectcosts[1][3]=999;
    connectcosts[2][0]=3;  connectcosts[2][1]=1;  connectcosts[2][2]=0;
    connectcosts[2][3]=2;
    connectcosts[3][0]=7;  connectcosts[3][1]=999;  connectcosts[3][2]=2;
    connectcosts[3][3]=0;

    # be nice: check if source and destination id's are reasonable
    if (packet.sourceid < 0) or (packet.sourceid > 3):
        print("WARNING: illegal source id in your packet, ignoring packet!\n")
        return
    if (packet.destid < 0) or (packet.destid > 3):
        print("WARNING: illegal dest id in your packet, ignoring packet!\n")
        return
    if (packet.sourceid == packet.destid):
        print("WARNING: source and destination id's the same, ignoring packet!\n")
        return
    if (connectcosts[packet.sourceid][packet.destid] == 999):
        print("WARNING: source and destination not connected, ignoring packet!\n")
        return

    # make a copy of the packet student just gave me since he/she may decide
    # to do something with the packet after we return back to him/her
    mypktptr = copy.deepcopy(packet)
    if TRACE > 2:
        print("    TOLAYER2: source: %d, dest: %d\n              costs:" %
              (mypktptr.sourceid, mypktptr.destid))
        for i in range(4):
            print("%d  " % (mypktptr.mincost[i]))
        print("\n")

    # create future event for arrival of packet at the other side
    evptr = Event(evtype=FROM_LAYER2, eventity=packet.destid, rtpktptr=mypktptr)

    # finally, compute the arrival time of packet at the other end.
    # medium can not reorder, so make sure packet arrives between 1 and 10
    # time units after the latest arrival time of packets
    # currently in the medium on their way to the destination
    lastime = clocktime
    for q in evlist:
        if ( (q.evtype == FROM_LAYER2)  and (q.eventity == evptr.eventity) ):
            lastime = q.evtime
    evptr.evtime =  lastime + 2. * random.uniform(0, 1)


    if TRACE > 2:
        print("    TOLAYER2: scheduling arrival on other side\n")
    insertevent(evptr)


if __name__ == '__main__':
    main()
