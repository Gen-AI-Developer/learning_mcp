import requests 
URL = "http://localhost:8000/mcp"
PAYLOAD = {
    "jsonrpc": "2.0",
    "method":"mcp",
    "params": {},
    "id": 1,
}
HEADER = {
    "Content-Type":"application/json",
    "Accept": "application/json, text/event-stream"
}
response = requests.post(URL,json=PAYLOAD,headers=HEADER,stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
        # decode bytes to string and print
        # for example you could parse json if the response is in json format
        # import json
        # data = json.loads(line.decode('utf-8'))
        # print(data) 