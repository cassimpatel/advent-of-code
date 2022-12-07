class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.subfolders = {}
        self.files = {}

    def printFolder(self, indent=0):
        indentation = "".join(['|  '] * indent)
        print(indentation +  '[FOLD] ' + self.name)
        for file in self.files:
            print(indentation + '|  [FILE] ' + file + ', size: ' + str(self.files[file]))
        for subfolder in self.subfolders:
            self.subfolders[subfolder].printFolder(indent+1)

    def calculateSize(self):
        if hasattr(self, 'size'):
            return self.size
        size = 0
        for file in self.files:
            size += self.files[file]
        for subfolder in self.subfolders:
            size += self.subfolders[subfolder].calculateSize()
        self.size = size
        # print(folder.name, size)
        return self.size

def generate_file_tree(cmds):
    rootNode = Folder('/')

    current_dir = rootNode
    parent_dir = None
    
    for cmd in cmds:
        splitCmd = cmd.split()

        if splitCmd[0] == '$' and splitCmd[1] == 'cd':
            if splitCmd[2] == '/':
                current_dir, parent_dir = rootNode, None
            elif splitCmd[2] == '..':
                current_dir = parent_dir
                parent_dir = current_dir.parent
            else:
                parent_dir = current_dir
                current_dir = current_dir.subfolders[splitCmd[2]]
        elif splitCmd[0] == '$' and splitCmd[1] == 'ls':
            pass
        elif splitCmd[0] == 'dir':
            dirName = splitCmd[1]
            current_dir.subfolders[dirName] = Folder(dirName, current_dir)
        else:
            fileName, fileSize = splitCmd[1], splitCmd[0]
            current_dir.files[fileName] = int(fileSize)
    
    return rootNode

def getFolderSizes(folder):
    sizes = [folder.size]
    for subfolder in folder.subfolders:
        sizes += getFolderSizes(folder.subfolders[subfolder])
    return sizes

def day7_part1(input):
    cmds = input.split('\n')
    fileTree = generate_file_tree(cmds)
    fileTree.calculateSize()

    folderSizes = getFolderSizes(fileTree)
    folderSizes = [x for x in folderSizes if x <= 100000]
    return sum(folderSizes)

def day7_part2(input):
    cmds = input.split('\n')
    fileTree = generate_file_tree(cmds)
    fileTree.calculateSize()

    folderSizes = getFolderSizes(fileTree)
    minFolderSizeToDelete = 30000000 - (70000000 - fileTree.size)
    folderSizes = [x for x in folderSizes if x >= minFolderSizeToDelete]
    return min(folderSizes)

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day7_part1(example_input) == 95437
    print(day7_part1(test_input))

    assert day7_part2(example_input) == 24933642
    print(day7_part2(test_input))