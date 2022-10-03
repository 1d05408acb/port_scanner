import socket
import re
import common_ports

# Check if the hostname is an IP address
def check_ip(hostname):
    if re.search(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) is None:
      return False
    else:
      return True

# Check which ports that is open on the target
def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    try:
      # Get ip by host
      ip_address = socket.gethostbyname(target)
      print("Target = {}".format(ip_address))
    except:
      # Error message if ip address is not retrieved.
      if check_ip(target) == True:
        return "Error: Invalid IP address."
      else:
        return "Error: Invalid hostname."

    if ip_address != target:
      Hostname = target
    else:      
      try:
        # Get the host by IP address
        Hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(target)
      except:
        Hostname = None
    
    for port in range(port_range[0], port_range[1]):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # Timeout so that you have a better flow when the script runs.
      sock.settimeout(1)
      result = sock.connect_ex((ip_address, port))
      if result == 0:
        print("Port {}: Open".format(port))
        open_ports.append(port)
      else:
        print("Port {}: Closed".format(port))
        pass
      sock.close()

    # Verbose mode
    if verbose==True:
      if Hostname is None:
        t = f"Open ports for {ip_address}\n"
      else:
        t = f"Open ports for {Hostname} ({ip_address})\n"
      t += "PORT     SERVICE"
      for port in open_ports:
        service_name = '-'
        if port in common_ports.ports_and_services:
          service_name = common_ports.ports_and_services[port]
        p = str(port)
        t+= "\n"+p + ' '*(9-len(p)) + service_name
        open_ports = t

    return(open_ports)