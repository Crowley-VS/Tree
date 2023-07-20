import os
from colorama import Fore, init

class Tree:
    def __init__(self):
        '''
        Initialize Tree with rendering chars and colors.
        '''
        self.rendering_chars = {'line': '│   ', 'middle': '├───', 'last': '└───', 'space': '    '} 
        self.dir_color = Fore.CYAN
        self.dir_color_reset = Fore.RESET
        
    def go_through(self, path: str, prefix: str = ''):
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

        try:
            entries = os.listdir(path)
        except FileNotFoundError:
            raise FileNotFoundError
        except OSError:
            raise OSError
        
        for entry in entries:
            num_entries+=1
            # Indicates whether the entry is the last one in the current level of the tree for a given directory.
            is_last_entry = num_entries == len(entries)


            if os.path.isdir(path+os.sep+entry):
                yield self.render_entry(prefix, entry, is_last=is_last_entry, is_directory=True)
                try:
                    if is_last_entry:
                        # If the entry is last, there's no need to keep rendering
                        # the line going down as there won't be any other entries.
                        # For that reason, 'space' from self.rendering chars is used for the prefix
                        yield from self.go_through(path+os.sep+entry, prefix = prefix + self.rendering_chars['space'])
                    else:
                        yield from self.go_through(path+os.sep+entry, prefix = prefix + self.rendering_chars['line'])
                except OSError:
                    # Yield the directory without going through it.
                    yield self.render_entry(prefix, entry, is_last=is_last_entry, is_directory=True)
            # Else - the entry is a file
            else:
                yield self.render_entry(prefix, entry, is_last=is_last_entry, is_directory=False)
        
    def render_entry(self, prefix: str, name: str, is_last: bool = False, is_directory: bool = False):
        """
        Render the formatted representation of an entry in the directory tree

        :param prefix: str string containing the indentation or prefix for the current level.
        :param name: str name of the entry (file or directory).
        :param is_last: bool, optional
            Indicates whether the entry is the last one in the current level of the tree.
            Defaults to False.
        :param is_directory: bool, optional
            Indicates whether the entry is a directory. If True, the directory name will be highlighted
            with a specified color. Defaults to False.
        :return: str
            A formatted string representation of the entry in the directory tree

        Example:
            Suppose we have the following directory structure:
            ├── dir1
            │   ├── file1.txt
            │   └── file2.txt
            └── dir2
                ├── file3.txt
                └── file4.tx        
            Calling render_entry('│   ', 'file3.txt') will return: '│   ├───file3.txt'
            Calling render_entry('    ', 'dir1', last=True, is_directory=True) will return: '    └───dir1'
        """
        if is_last:
            rendering_char = self.rendering_chars['last']
        else:
            rendering_char = self.rendering_chars['middle']

        if is_directory:
            color_start = self.dir_color
            color_reset = self.dir_color_reset
        else:
            color_start = ''
            color_reset = ''

        return '{}{}{}{}{}'.format(prefix, rendering_char, color_start, name, color_reset)

class Menu:
    def __init__(self):
        '''
        Initialize a terminal menu.
        '''
        self.tree = Tree()
    def main(self):
        '''
        Start the Tree script in terminal.
        Display prompts and proccess the path given when run.
        '''
        print('\nTree\n')
        while True:
            print('(In order to exit, enter \'q\')')
            path = input('Please enter a path: ')
            if path == 'q':
                break
            try:
                for result in self.tree.go_through(path):
                    print(result)
            except FileNotFoundError:
                print('Tree can\'t find the path specified.')
            except OSError:
                print('Invalid path specified.')
        
if __name__ == '__main__':
    Menu().main()
