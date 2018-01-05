import os

def getFileAndDirec(path):
    for f in (os.walk(path)):
        for file in f:
            print(file)
#     for f in arr:
#         print(f)

def getFile(path):
    for f in os.walk(path)[2]:
        for file in f:
            print(file)
#     for f in arr:
#         print(f)

def getListdir(path):
    arr = os.listdir(path)
    for f in os.listdir(path):
        path_file = path + '/' + f
        # print os.path.isdir(f)
        print os.path.isfile(path_file)
    print arr

def main():
    path = '/Users/administrator/Desktop/python-quickstart-master/test'
    getFile(path)

if __name__ == '__main__':
    main()
