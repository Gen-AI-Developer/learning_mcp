# with is keyword used for context Managers, we open and close sessions
#  by using it. 
#  Now here we are opening and closing the file by using with keyword, it
# opens a file for 'r' permissions which means read, so with keyword will
# safely open a file for read session and close it.
with open("data.txt", 'r') as data:
    textdata = data.readlines()
    for content in textdata:
        print(content)

with open("output.txt","w",) as wrt:
    outfile = wrt.writelines("lines")



with open("data.txt","r") as read_data, open("output.txt","w") as write_data:
    data = read_data.readlines()
    output =write_data.writelines(data)