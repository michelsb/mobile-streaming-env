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
    
	sta1 = net.addStation('sta1', cls=DockerSta, dimage="michelsb/ubuntu20-wifi",  antennaHeight='1', antennaGain='5')
	sta2 = net.addStation('sta2', cls=DockerSta, dimage="michelsb/ubuntu20-wifi",  antennaHeight='1', antennaGain='5')
    
	ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
                             failMode="standalone", position='50,50,0')
	
	
	h1 = net.addDocker('h1', dimage="michelsb/ubuntu20-wifi", cpu_period=50000, cpu_quota=25000)
	#c1 = net.addController('c1')

	info("*** Configuring propagation model\n")
	net.setPropagationModel(model="logDistance", exp=4.5)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	if '-p' not in args:
	    net.plotGraph(max_x=300, max_y=300)

	net.setMobilityModel(time=0, model='RandomWayPoint', max_x=100, max_y=100,
                         min_v=0.5, max_v=0.5, seed=20)

	info("*** Creating links\n")
	net.addLink(ap1, h1)
	
	info("*** Starting network\n")
	net.addNAT(linkTo='ap1').configDefault()
	net.build()
	#c1.start()
	ap1.start([c1])

	# set_socket_ip: localhost must be replaced by ip address
	# of the network interface of your system
	# The same must be done with socket_client.py
	info("*** Starting Socket Server\n")
	net.socketServer(ip='127.0.0.1', port=12345)

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology(sys.argv)
