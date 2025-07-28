# with is keyword used for context
with open("data.txt", 'r') as data:
    textdata = data.readlines()
    for content in textdata:
        print(content)

with open("output.txt","w",) as wrt:
    outfile = wrt.writelines("lines")



with open("data.txt","r") as read_data, open("output.txt","w") as write_data:
    data = read_data.readlines()
    output =write_data.writelines(data)