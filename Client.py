from opcua import Client
import Server

# shortcuts
URL = Server.URL
NAME = Server.NAME
NAMESPACE = Server.NAMESPACE

def make_client():
    client = Client(URL)
    client.register_namespace(Server.NAMESPACE)

