from twisted.web import server, resource
from twisted.internet import reactor, serialport
from twisted.protocols import basic
import os

class Values:
    def __init__(self):
        self.value = 0
        self.th_list = None
        self.ldict = {}

    def set_value(self, value):
        self.value = value

    def inc_value(self, value):
        self.value += value

    def get_value(self):
        return self.value

    def set_list(self, values):
        self.th_list = values

    def get_list(self):
        return self.th_list

    def set_dict(self, vals):
        key = vals[2]
        self.ldict[key] = vals

    def get_dict(self):
        return self.ldict

class Webmin(resource.Resource):
    isLeaf = True
    def __init__(self):
        self.values = global_values
        self.column_dict = {'uCTime':0,
               'sequenceNumber':1,
               'circuitID':2,
               'isOn':3,
               'VRMS':4,
               'IRMS':5,
               'VPEAK':6,
               'IPEAK':7,
               'PERIODUS':8,
               'VA':9,
               'W':10,
               'VAEnergy':11,
               'WEnergy':12,
               'PFactor':13,
               'VA_ACCUM':14,
               'W_ACCUM':15,
               'errorNum':16}
        self.column_list = ['uCTime', 'sequenceNumber', 'circuitID', 'isOn',
               'VRMS',
               'IRMS',
               'VPEAK',
               'IPEAK',
               'PERIODUS',
               'VA',
               'W',
               'VAEnergy',
               'WEnergy',
               'PFactor',
               'VA_ACCUM',
               'W_ACCUM',
               'errorNum']



    def render_GET(self, request):
        #ATME = self.service.ATME
        #return 'value = ' + str(self.values.get_value()) + '\n' + str(self.values.get_list()) + '\n'
        response = ''
        thedict = self.values.get_dict()
        response += '<table border="1">\n'
        response += "<tr>\n"
        for c in self.column_list:
            response += "<td>" + str(c) + "</td>\n"
        response += "</tr>\n"
        keys = thedict.keys()
        keys.sort()
        for key in keys:
            response += "<tr>\n"
            for s in thedict[key]:
                response += "<td>" + str(s) + "</td>\n"
            response += '</tr>\n'
        response += "</table>\n"
        return response

class Echo(basic.LineReceiver):
    def __init__(self):
        # get accumulator from database
        self.accumulator = 0
        #self.values = Values()
        self.values = global_values
    def lineReceived(self, line):
        vals = line.split(',')
        if len(vals) > 2:
            if vals[2].isdigit():
                #print
                #print 'circuit #', vals[2]
                #print 'W', vals[10]
                #print 'VA', vals[9]
                #print vals
                self.values.inc_value(int(vals[8]))
                self.values.set_list(vals)
                self.values.set_dict(vals)
        #acc = int(vals[0])
        #self.accumulator += acc
        #print self.accumulator
        #print vals
        return


if __name__ == '__main__':

    global_values = Values()
    PORT = 8080

    baudrate = 9600
    port = '/dev/ttyUSB0'
    s = serialport.SerialPort(Echo(), port, reactor, baudrate=baudrate)
    
    reactor.listenTCP(PORT, server.Site(Webmin()))
    reactor.run()


column_dict = {'uCTime':0,
               'sequenceNumber':1,
               'circuitID':2,
               'isOn':3,
               'VRMS':4,
               'IRMS':5,
               'VPEAK':6,
               'IPEAK':7,
               'PERIODUS':8,
               'VA':9,
               'W':10,
               'VAEnergy':11,
               'WEnergy':12,
               'PFactor':13,
               'VA_ACCUM':14,
               'W_ACCUM':15,
               'errorNum':16}
'''
Order & Title          & Units     & Code Variable  & ADE Variable \\
0     & uCTime         &           &                & ---          \\
1     & sequenceNumber &           &                & ---          \\
2     & circuitID      &           &                & ---          \\
3     & isOn           &           &                & ---          \\
4     & VRMS           &           & c--$>$VRMS     &              \\
5     & IRMS           &           & c--$>$IRMS     &              \\
6     & VPEAK          &           & c--$>$vpeak    & RSTVPEAK     \\
7     & IPEAK          &           & c--$>$ipeak    & RSTIPEAK     \\
8     & PERIODUS       &           & c--$>$periodus &              \\
9     & VA             &           & c--$>$VA       & LVAENERGY    \\
10    & W              &           & c--$>$W        & LAENERGY     \\
11    & VAEnergy       & Joules?   & c--$>$VAEnergy & RVAENERGY     \\
12    & WEnergy        & Joules?   & c--$>$WEnergy  & RAENERGY     \\
13    & PFactor        &           & c--$>$PF       &              \\
14    & VA ACCUM       &           & TODO        \\
15    & W ACCUM        &           & TODO        \\
16    & errorNum       &           &             \\
'''
