from distance_vector import Rtpkt, TRACE, YES, NO


class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]

dt3 = DistanceTable()

# students to write the following two routines, and maybe some others

def rtinit3():
    pass


def rtupdate3(rcvdpkt):
    pass

def printdt3(dtptr):
    print("             via     \n")
    print("   D3 |    0     2 \n")
    print("  ----|-----------\n")
    print("     0|  %3d   %3d\n", dtptr.costs[0][0], dtptr.costs[0][2])
    print("dest 1|  %3d   %3d\n", dtptr.costs[1][0], dtptr.costs[1][2])
    print("     2|  %3d   %3d\n", dtptr.costs[2][0], dtptr.costs[2][2])
