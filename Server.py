from opcua import Server, Node
import time

URL = 'opc.tcp://157.138.24.165:4840'
NAME = 'testserver'
NAMESPACE = 'testnamespace'


def setup():

    # istanzia la classe server
    server = Server()
    print("starting")
    server.set_endpoint(URL)  # setta il punto di ascolto
    server.set_server_name(NAME)  # setta il nome del server

    # Registra un namespace. Un namespace è un container per i nodes del server
    # Il valore ritornato è il numero dei namespace registrati
    # Doc: https://reference.opcfoundation.org/v104/Core/docs/Part3/8.2.2/
    space = server.register_namespace(NAMESPACE)
    # Estrae il primo Node per gli oggetti. Un Node può essere visto come un container per le variabili del namespace
    node = server.get_objects_node()

    param = node.add_object(space, "Parameters")
    text = param.add_variable(space, "Text variable", "String of text")
    _int = param.add_variable(space, "Integer variable", 1102)
    print("starting")

    while True:
        print(text.mro)
        print(_int)
        time.sleep(1)


if __name__ == "__main__":
    setup()
