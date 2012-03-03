from twisted.web import server, resource
from twisted.internet import reactor, serialport
from twisted.protocols import basic
import os


class Values:
    def __init__(self):
        self.ldict = {}

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


class ATMEReceiver(basic.LineReceiver):

    def __init__(self):
        self.values = global_values

    def lineReceived(self, line):
        vals = line.split(',')
        if len(vals) > 2:
            if vals[2].isdigit():
                self.values.set_dict(vals)
        return


if __name__ == '__main__':

    global_values = Values()

    baudrate = 9600
    ATME_port = '/dev/ttyUSB0'
    s = serialport.SerialPort(ATMEReceiver(),
                              ATME_port,
                              reactor,
                              baudrate=baudrate)

    PORT = 8080
    reactor.listenTCP(PORT, server.Site(Webmin()))
    reactor.run()
