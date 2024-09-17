import socket
from dnslib import DNSRecord, QTYPE, RR, A
from logger import logger
import threading

class DNSServer:
    def __init__(self, ip):
        self.ip = ip
        self.running = False
        self.socket = None

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 53))
        self.running = True
        
        logger.info(f"Started DNS Server on {self.ip}")

        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                threading.Thread(target=self.handle_dns_query, args=(data, addr)).start()
            except socket.error:
                if not self.running:
                    break
                logger.error("Socket error in DNS server")

        self.socket.close()
        logger.info("DNS Server stopped")

    def handle_dns_query(self, data, addr):
        try:
            d = DNSRecord.parse(data)
            reply = d.reply()
            
            for question in d.questions:
                reply.add_answer(RR(question.qname, QTYPE.A, rdata=A(self.ip), ttl=60))

            self.socket.sendto(reply.pack(), addr)
            logger.debug(f"Redirected DNS query for {question.qname} to {self.ip}")
        except Exception as e:
            logger.error(f"Error handling DNS query: {e}")

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()

if __name__ == "__main__":
    dns_server = DNSServer("10.10.1.1")
    dns_server.run()