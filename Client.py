from opcua import Client
import Server

# shortcuts
URL = Server.URL
NAME = Server.NAME
NAMESPACE = Server.NAMESPACE
# da ricordare ma da eliminare
def make_client():
    client = Client(URL)
    client.connect()
    print("connected")
    nodes = client.get_namespace_array()
    print(nodes)
    omron_server = str(nodes[2])

if __name__ == '__main__':
    make_client()