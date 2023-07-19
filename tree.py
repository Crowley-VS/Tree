import os
from pathlib import Path
from colorama import Fore, init

class Tree:
    def __init__(self):
        '''
        Initialize Tree with rendering chars and colors.
        '''
        self.rendering_chars = {'line': '│   ', 'middle': '├───', 'last': '└───', 'space': '    '} 
        self.dir_color = Fore.CYAN
        self.dir_color_reset = Fore.RESET
    def go_through(self, path, prefix = ''):
        '''
        Create a generator for the contents of the path specified
        rendering appropriate indentation for directories and entries.
        Highlight directory names.
        
        :param path: str path to be processed
        :param prefix: prefix to be used for rendering.
            There is no need to pass a prefix when the function is called by another interface
        '''
        # Num of the checked entries
        num_entries=0
        entries = os.listdir(path)
        for entry in entries:
            num_entries+=1
            # If the func is on the last entry
            if len(entries)==num_entries: 
                # If the entry is a directory
                if os.path.isdir(path+os.sep+entry):
                    yield prefix + self.rendering_chars['last'] + self.dir_color + entry

                    try:
                        # If the entry is last, there's no need to keep rendering
                        # the line going down as there won't be any other entries.
                        # For that reason, 'space' from self.rendering chars is used
                        yield from self.go_through(path+os.sep+entry, prefix = prefix + self.rendering_chars['space'])
                    # If the directory is private.
                    except OSError:
                        # Yield the directory without going through it.
                        yield prefix + self.rendering_chars['last'] + self.dir_color + entry
                # Else - the entry is a file
                else:
                    yield prefix + self.rendering_chars['last'] + entry
            
            else:
                # If the entry is a directory
                if os.path.isdir(path+os.sep+entry):
                    yield prefix + self.rendering_chars['middle'] + self.dir_color + entry
                    try:
                        yield from self.go_through(path+os.sep+entry, prefix = prefix + self.rendering_chars['line'])
                    except OSError:
                        # Yield the directory without going through it.
                        yield prefix + self.rendering_chars['middle'] + self.dir_color + entry
                # Else - the entry is a file
                else:
                    yield prefix + self.rendering_chars['middle'] + entry
    def main(self):
        '''
        Start the Tree script.
        '''
        # Auto reset colors
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
