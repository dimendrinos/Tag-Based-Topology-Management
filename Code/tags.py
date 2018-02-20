from pox.core import core
import pox.openflow.nicira as nx
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr6,EthAddr 

log = core.getLogger()

"""
For that topology: 

h1 ---0001---s1---0010---s2---0100---h2
https://openflow.stanford.edu/display/ONL/POX+Wiki
http://flowgrammable.org/sdn/openflow/message-layer/match/#tab_ofp_1_2

POX SDN Controller. Creating forwarding rules according to the Topology of the Network 
using Topology Manager to define a destination based on a tag. Topology Manager will return
bloom filter id and here we initialize the rules at the IP Layer.
"""

class Tags (object):
  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)
    if (connection.eth_addr.toStr() == "00:00:00:00:00:01"):
        # Rules for switch s1 !

        '''
        Table id is a number for the the table of rules for each switch.
        Priority is for overlapping matches. Higher values are higher priority.
        in_port - If using a buffer_id, this is the associated input port.
        match - An ofp_match object. By default, this matches everything,
        so you should probably set some of its fields!
        
        '''

        print "Preparing of rules"


        msg = nx.nx_flow_mod_table_id()
        connection.send(msg)
        #table 0 - Rules for IP :01

        '''
        
        Forward a packet to source if the port that is coming is the same as the input
        
        '''

        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 1500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.of_in_port = 1
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)

        '''
             When a message comes to the Switch if has a rule for this IPv6 
             forward it to next port 
        '''

        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 1000
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.nx_ipv6_dst = (IPAddr6("::1"),IPAddr6("::1"))
        msg.actions.append(of.ofp_action_output(port = 1 ))
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)

        '''
        
        If you have no rule for this IP check 
        table 1 for IP :02
        
        '''

        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        
        #table 1 - Rules for IP :02
        msg = nx.nx_flow_mod()
        msg.table_id = 1
        msg.priority = 1000
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.nx_ipv6_dst = (IPAddr6("::2"),IPAddr6("::2"))
        msg.actions.append(of.ofp_action_output(port = 1))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 1
        msg.priority = 1500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.of_in_port = 2
        self.connection.send(msg)
        
    if (connection.eth_addr.toStr() == "00:00:00:00:00:02"):
        # Rules for switch s2  !
        print "Preparing of rules"

        '''
        
        The same Rules also for Switch 2 check the above comments
        
        '''

        msg = nx.nx_flow_mod_table_id()
        connection.send(msg)
        #table 0      
        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 1500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.of_in_port = 1
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 1000
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.nx_ipv6_dst = (IPAddr6("::2"),IPAddr6("::2"))
        msg.actions.append(of.ofp_action_output(port = 1 ))
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 0
        msg.priority = 500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.actions.append(nx.nx_action_resubmit.resubmit_table(table = 1))
        self.connection.send(msg)
        #table 1
        msg = nx.nx_flow_mod()
        msg.table_id = 1
        msg.priority = 1000
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.nx_ipv6_dst = (IPAddr6("::4"),IPAddr6("::4"))
        msg.actions.append(of.ofp_action_output(port = 2 ))
        self.connection.send(msg)
        
        msg = nx.nx_flow_mod()
        msg.table_id = 1
        msg.priority = 1500
        msg.match.of_eth_dst = "00:00:00:00:00:00"
        msg.match.of_eth_type = 0x86dd
        msg.match.of_in_port = 2
        self.connection.send(msg)


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """



def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    Tags(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
