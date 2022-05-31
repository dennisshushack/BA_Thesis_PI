import requests
from requests.auth import HTTPBasicAuth

# Create a POST request on 192.168.0.249:5000/rest/training with Basic Auth:
# username: admin
# password: admin
# and data: {device = 000000005426d851 category = training ml_type = anomaly monitors = ['m1', 'm2', 'm3'] behavior = normal path =/home/dennis/Documents/data/000000005426d851/anomaly/training}
localhost = '192.168.0.249:5000'
username = 'admin'
password = 'admin'
serial = '000000005426d851'
category = 'testing'
ml_type = 'anomaly'
monitors = ['m1', 'm2', 'm3']
behavior = 'ransom1'
path = '/home/dennis/Documents/data/000000005426d851/anomaly/testing'
response = requests.post("http://{localhost}/rest/train".format(localhost=localhost), auth=HTTPBasicAuth('admin', 'admin'), json={"ml_type": ml_type, "monitors": monitors, "behavior": behavior, "category": category, "path": path, "device": serial})



