from scapy.all import sr1, IP, ICMP

class ServerChecker:
    def ping_server(self, server):
        response = sr1(IP(dst=server.ip) / ICMP(), timeout=2)
        if response:
            return "Online"
        return "Offline"
