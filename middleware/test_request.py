import requests
from requests.auth import HTTPBasicAuth

# Create a POST request on 192.168.0.249:5000/rest/training with Basic Auth:
# m1 = RES, m2=KERN, m3 = SYS
# username: admin
# password: admin
# and data: {device = 000000005426d851 category = training ml_type = anomaly monitors = ['m1', 'm2', 'm3'] behavior = normal path =/home/dennis/Documents/data/000000005426d851/anomaly/training}
localhost = '127.0.0.1:5000'
username = 'admin'
password = 'admin'
serial = '00000000fd4336c8'
category = 'testing'
ml_type = 'classification'
monitors = "KERN,SYS,RES"
behavior = 'normal'
path = '/home/dennis/Documents/data_popos/00000000fd4336c8/classification/testing'
description = "normal"
number = 6
begin = 1222
end = 1223
response = requests.post("http://{localhost}/rest/main".format(localhost=localhost), auth=HTTPBasicAuth('admin', 'admin'), json={"ml_type": ml_type, "experiment": description, "monitors": monitors, "behavior": behavior, "category": category, "path": path, "device": serial, "begin": None, "end": None, "number": number})



