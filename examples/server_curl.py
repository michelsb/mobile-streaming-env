#!/usr/bin/python

'This example show how to configure Propagation Models'

import sys

from mininet.log import setLogLevel, info, debug
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.net import Containernet
from containernet.node import Node

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

def topology(args):

	"Create a network."
	net = Containernet()

	info("*** Creating nodes\n")
	for n in range(1, 3):
		net.addCar('car%d' % n, mac='00:00:00:00:00:%02d' % n, ip='10.0.0.%d/8' % n, defaultRoute='via 10.0.0.254', position='%s,40,0' % (45+n), cls=DockerSta, dimage="michelsb/alpine-wifi")
	sta1 = net.addStation('sta1', mac='00:00:00:00:00:10', ip='10.0.0.10/8', defaultRoute='via 10.0.0.254', position='10,45,0', cls=DockerSta, dimage="michelsb/alpine-wifi")	
	ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='6', failMode="standalone", mac='00:00:00:00:01:00', position='70,50,0')
	ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='11', failMode="standalone",mac='00:00:00:00:02:00', position='10,50,0')
	c1 = net.addController('c1')	
	server = net.addDocker('server', ip='192.168.1.100/24', dimage="michelsb/alpine-wifi", defaultRoute='via 192.168.1.254')	
	
	info('*** Adding switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	
	info('*** Adding routers\n')
	defaultIP = '192.168.1.254/24'  # IP address for r0-eth1
	router = net.addHost( 'r0', cls=LinuxRouter, ip=defaultIP)
	
	info("*** Configuring propagation model\n")
	net.setPropagationModel(model="logDistance", exp=5)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	info("*** Associating and Creating links\n")	
	net.addLink(s1, router, intfName2='r0-eth1', params2={ 'ip' : defaultIP } )  # for clarity
	net.addLink(s2, router, intfName2='r0-eth2',params2={ 'ip' : '10.0.0.254/8' } )
	
	net.addLink(server, s1)
	net.addLink(s2, ap1)		
	net.addLink(s2, ap2)	
	
	if '-p' not in args:
	    net.plotGraph(max_x=120, max_y=120)	

	info("*** Starting network\n")	
	net.start()
	
	info( '*** Routing Table on Router:\n' )
	print((net['r0'].cmd('route')))

	info("*** Starting Socket Server\n")
	net.socketServer(ip='127.0.0.1', port=12345)

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology(sys.argv)
