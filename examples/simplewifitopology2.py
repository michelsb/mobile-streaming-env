#!/usr/bin/python

'This example creates a simple network topology with 1 AP and 2 stations'

import sys

from containernet.net import Containernet
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.term import makeTerm
from mininet.log import info, setLogLevel


def topology():
	"Create a network."
	net = Containernet()

	info("*** Creating nodes\n")
	sta_arg = dict()
	ap_arg = dict()
	if '-v' in sys.argv:
		sta_arg = {'nvif': 2}
	else:
		# isolate_clientes: Client isolation can be used to prevent low-level
		# bridging of frames between associated stations in the BSS.
		# By default, this bridging is allowed.
		# OpenFlow rules are required to allow communication among nodes
		ap_arg = {'client_isolation': True}

	info('*** Adding docker containers\n')
	sta1 = net.addStation('sta1', ip='10.0.0.3', mac='00:02:00:00:00:10',
                          cls=DockerSta, dimage="michelsb/ubuntu20-wifi", cpu_shares=20, **sta_arg)
	sta2 = net.addStation('sta2', ip='10.0.0.4', mac='00:02:00:00:00:11',
                          cls=DockerSta, dimage="michelsb/ubuntu20-wifi", cpu_shares=20)
	ap1 = net.addAccessPoint('ap1', ssid="simpletopo", mode="g",
                             channel="5", **ap_arg)
	c0 = net.addController('c0')
	
	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	#info("*** Associating Stations\n")
	#net.addLink(sta1, ap1)
	#net.addLink(sta2, ap1)

	info("*** Starting network\n")
	net.build()
	c0.start()
	ap1.start([c0])

	if '-v' not in sys.argv:
		ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,arp,in_port=1,'
                'actions=output:in_port,normal"')
		ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,icmp,in_port=1,'
                'actions=output:in_port,normal"')
		ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,udp,in_port=1,'
                'actions=output:in_port,normal"')
		ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,tcp,in_port=1,'
                'actions=output:in_port,normal"')

	#sta1.cmd('iw dev sta1-wlan0 connect simpletopo')
	#sta2.cmd('iw dev sta2-wlan0 connect simpletopo')

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology()
