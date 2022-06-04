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
category = 'training'
ml_type = 'classification'
monitors = "m1,m2,m3"
behavior = 'normal'
path = '/home/dennis/Documents/data/000000005426d851/classification/training'
description = "test1"
begin = 1222
end = 1223
response = requests.post("http://{localhost}/rest/main".format(localhost=localhost), auth=HTTPBasicAuth('admin', 'admin'), json={"ml_type": ml_type, "experiment": description, "monitors": monitors, "behavior": behavior, "category": category, "path": path, "device": serial, "begin": None, "end": None})



