import threading
import datetime
from opcua import Client

IP = "localhost"
PORT = "5000"     
URL = "opc.tcp://" + IP + ":" + PORT

NAME = "OPCUAtestserver"
NAMESPACE = "OPCUAtestnamespace"
"""

         struttura generale di un server secondo OPCUA

    -------------------------namespace----------------------------
    | ---------------------------------------------------------- |                                                                 
    |                      address space                         |
    | ---------------------------------------------------------- |                                                                 
    |        |                            |                      |                                                                 
    |        |                            |                      |                                                                 
    |        |                            |                      |                                                                 
    |        V                            V                      |                                                                 
    |      node 1                      node n..                  |                                                                 
    |      |-> variabili                                         |                                                                 
    |      |-> oggetti                                           |                                                                 
    |      |-> metodi                                            |                                                                 
    |                                                            |                                                                 
    |                                                            |                                                                 
    |                                                            |                                                                 
    |                                                            |       
    --------------------------------------------------------------   
                                                           
"""


def testclient():

    client = Client(URL)
    try:
        # la connessione del client lancerà un errore se dovesse fallire, ma la disconnessione ne lancerà un altro
        print("start")
        client.connect()

        # estrazione del root node dal client. Il root node è il contenitore delle variabili (e dei nodi) 
        # per quell' address space
        root = client.get_root_node()
        print("root = " + str(root))

        # ottiene i "figli" del nodo radice. Questi possono essere altri Nodes, oggetti, variabili e metodi.
        children = root.get_children()
        print("children = " + str(children))

    except Exception: 
        print("["+str(datetime.date)+"]:" + threading.current_thread().name + " produced exception. Terminating")

    finally:    
        client.disconnect()  # importante sconnettere il client


if __name__ == '__main__':
    testclient()
