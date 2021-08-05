from Monitor import Monitor as Reader
from ClientPack.Wr_client import Actor as Writer

exit_success = 1
exit_failure = 0

r = Reader(1)
wr = Writer("uname", "pw")
rdonly_name = "Fotocellula"
wr_name = "LED_Yellow"

try:

    print("Var" + wr_name + " = " + str(wr.get_variable(wr_name)))
    wr.set_variable(wr_name, False)

    wr.set_variable(rdonly_name, True)
    print("Error occurred")

except Exception:

    print("Error caught")
    exit(exit_failure)

finally:
    wr = None
    r = None

exit(exit_success)
