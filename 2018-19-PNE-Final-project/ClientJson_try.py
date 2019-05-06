import http.client
import json

PORT = 8000
SERVER = 'localhost'

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

conn = http.client.HTTPConnection(SERVER, PORT)


# 1 TRY FOR JSON
conn.request("GET", "/listSpecies?json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

# 2 TRY FOR JSON
conn.request("GET", "/karyotype?specie=mouse&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

# 3 TRY FOR JSON
conn.request("GET", "/chromosomeLength?specie=mouse&chromo=18&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

# 4 TRY FOR JSON
conn.request("GET", "/geneSeq?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

# 5 TRY FOR JSON
conn.request("GET", "/geneInfo?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

# 6 TRY FOR JSON
conn.request("GET", "/geneCalc?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

# 7 TRY FOR JSON
conn.request("GET", "/geneList?chromo=1&start=0&end=30000&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)