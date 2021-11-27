import os
from pathlib import Path
from colorama import Fore, init

class Tree:
    def __init__(self):
        '''Initialize Tree with rendering chars and colors.'''
        self.rendering_chars = {'line': '│   ', 'middle': '├───', 'last': '└───', 'space': '    '} 
        self.dir_color = Fore.CYAN
        self.dir_color_reset = Fore.RESET
    def go_through(self, _path, prefix = ''):
        '''Go through the contents of the path and yield them.
        Change colors of the directory names.'''
        num_files=0 #num of the times the func went through the files
        files = os.listdir(_path)
        for file in files:
            num_files+=1
            if len(files)==num_files: #if the func is on the last file
                if os.path.isdir(_path+os.sep+file):
                    yield prefix + self.rendering_chars['last'] + self.dir_color + file
                    #if the file is last, there's no need to keep rendering the line going down as there won't be any other files
                    yield from self.go_through(_path+os.sep+file, prefix = prefix + self.rendering_chars['space'])
                else:
                    yield prefix + self.rendering_chars['last'] + file
            else:
                if os.path.isdir(_path+os.sep+file):
                    yield prefix + self.rendering_chars['middle'] + self.dir_color + file
                    yield from self.go_through(_path+os.sep+file, prefix = prefix + self.rendering_chars['line'])
                else:
                    yield prefix + self.rendering_chars['middle'] + file
    def main(self):
        '''Start the Tree script.'''
        init(autoreset=True)
        print('Tree')
        while True:
            print('(In order to exit, enter \'q\')')
            path = input('Please enter a path: ')
            if path == 'q':
                break
            try:
                for result in self.go_through(path):
                    print(result)
            except FileNotFoundError:
                print('Tree can\'t find the path specified.')
        
if __name__ == '__main__':
    Tree().main()
