#!/usr/bin/env python3


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

# possible events:
FROM_LAYER2 = 2
LINK_CHANGE = 10
