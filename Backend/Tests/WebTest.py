class Mockrequest:
    config = {"SECRET_KEY": "secret key"}


app = Mockrequest()
username = "name"
password = "pws"

payload = {
    "NAME": "name",
    "VALUES": str([21, 32, 432]),
    "STRUCT": {}
}
