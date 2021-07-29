from opcua import Server, Node
import time

URL = "opc.tcp://192.168.1.5:4851"
NAME = "testserver"
NAMESPACE = "testnamespace"


def setup():
    # apre il server su un dato URL definito dal PLC
    server = Server(URL)
    server.set_endpoint(URL) # setta il punto di ascolto
    server.set_server_name(NAME)# setta il nome del server

    space = server.register_namespace(NAMESPACE)
    node = server.get_objects_node()

    param: Node = node.add_object(space, "Parameters")

    text = param.add_variable(space, "Text variable", "String of text")
    _int = param.add_variable(space, "Integer variable", 1102)

    while True:
        print(text.mro)
        print(_int.mro)
        time.sleep(1)


if __name__ == "__main__":
    setup()
