#!/usr/bin/python

'This example show how to configure Propagation Models'

import sys

from mininet.log import setLogLevel, info, debug
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.net import Containernet


def topology(args):

	"Create a network."
	net = Containernet()

	info("*** Creating nodes\n")    
    
	sta1 = net.addStation('sta1', cls=DockerSta, dimage="michelsb/alpine-wifi",  antennaHeight='1', antennaGain='5')
	sta2 = net.addStation('sta2', cls=DockerSta, dimage="michelsb/alpine-wifi",  antennaHeight='1', antennaGain='5')
    
	ap1 = net.addAccessPoint('ap1', ssid='newssid', model='DI524',
                             mode='g', channel='1', position='50,50,0')
	c1 = net.addController('c1')

	info("*** Configuring propagation model\n")
	net.setPropagationModel(model="logDistance", exp=4)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	if '-p' not in args:
	    net.plotGraph(max_x=100, max_y=100)

	net.setMobilityModel(time=0, model='RandomWayPoint', max_x=100, max_y=100,
                         min_v=0.5, max_v=0.5, seed=20)

	info("*** Starting network\n")
	net.build()
	c1.start()
	ap1.start([c1])

	#sta1.cmd('iw dev sta1-wlan0 connect newssid')
	#sta2.cmd('iw dev sta2-wlan0 connect newssid')

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology(sys.argv)
