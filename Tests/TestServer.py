#   Questo file non serve a nessuno scopo specifico. è un server "dummy"  da usare per comprendere meglio OPCUA
import time

import TestClient
import random
import traceback

import opcua
from opcua import Node, Server, uamethod, ua

URL = TestClient.URL
NAME = TestClient.NAME
NAMESPACE = TestClient.NAMESPACE

running = False  # TODO : debug only


@uamethod
def method_for_server(boolvar):
    boolvar.set_value(not boolvar.get_value())


class Dummyobject:
    """
        Test object
    """

    # Costruttore dell'oggetto. Tutti i metodi non statici iniziano con "self"
    def __init__(self, stuff):
        self.__num__ = 0
        print("Dummy object")

    def dosomething(self):
        self.__num__ = random.Random.randint(1, 100)
        print(self.__num__)

    # Override di "ToString()"
    def __str__(self):
        return "Dummyobject"

    # Override di "Equals"
    def __eq__(self, other):
        return self.__str__() == other.__str__


    def v(self, a , b=None):
        self.v(b = 0 , a = 10)
        self.v(b = a , a = b)

        return 0 

def testserver():
    def printvar(var: Node):
        print(var.get_data_type() + ":" + var.get_value())

    server = Server()

    # Modifica dei dati nel server. Va fatto PRIMA dello start
    server.set_endpoint(URL)  # -> void ; punto di ascolto
    server.set_server_name(NAME)  # -> void; nome del server
    index = server.register_namespace(NAMESPACE)  # int; indice del namespace registrato

    try:

        print("started")

        # Nodo dati del server
        obj_node = server.get_objects_node()
        print("got rootnode")

        # AddObject crea un nuovo "oggetto" di campi e metodi non definiti. Al ritorno di questa operazione viene dato
        # un node corrispondente al contenitore di quell'oggetto, in cui possono essere inseriti variabili e metodi.

        e: Node = obj_node.add_object(index, "NewObject")  # Istanzio lo spazio per l'oggetto

        intvar: Node = e.add_variable(index, "Floatvar", float(20))  # Creo un primo campo float

        boolvar: Node = e.add_variable(index, "Boolvar", False)  # Creo un secondo campo booleano a cui do un setter

        print("Variables added")

        # Aggiungere un metodo a un oggetto è più verboso. Non vi è un numero finito di argument da passargli, ma
        # ho notato su tutti gli esempi che ho trovato che sono massimo 5
        negator = obj_node.add_method(
            index,  # Namespace a cui aggiungerlo
            "Negate_Boolean",  # Nome server side del metodo
            method_for_server,  # Metodo effettivo
            [opcua.ua.VariantType.Boolean],  # Tipo del dato in entrata
            [opcua.ua.VariantType.Boolean]  # Tipo di ritorno

        )
        print("Method added")
        server.start()

        intvar.set_read_only()  # Permette la sola lettura. Una tentata scrittura lancia un errore
        boolvar.set_writable()  # Abilita la scrittura a runtime. Potenzialmente molto insicuro

        print(str(boolvar) + " set to writeable. Calling method")
        try:
            negator.call_method(boolvar)
            obj_node.call_method(negator, boolvar)
        except Exception    :
            traceback.print_exc()

        while True:
            printvar(intvar.get_value())
            printvar(boolvar.get_value())
            time.sleep(5)
    except Exception as exc:

        print("Server exception occurred : " + str(exc))

    finally:
        server.stop()
        print("stopped")
        # ^ESTREMAMENTE IMPORTANTE. Se il server non viene spento resterà
        # a girare a vuoto fino a reboot del sistema


if __name__ == '__main__':
    testserver()
    print("DONE!")
