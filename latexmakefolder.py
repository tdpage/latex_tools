#!/usr/bin/env python 

#MIT License

#Copyright (c) 2020, 2021 Thomas Page

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


import argparse
import os
import sys
import pwd
from datetime import datetime


class latexmakefolder():
    def __init__(self):
        
        # specify some meta information
        self.CUR_USR = pwd.getpwuid(os.getuid()).pw_name
        self.TIMESTAMP = datetime.now().strftime('%d/%m/%Y %I:%M %p') + ' by ' + self.CUR_USR
        
        self.file_contents = str()
        
        # set the arguments 
        self.parser = argparse.ArgumentParser(description='Create a new LaTeX document directory and base document.',
                                              epilog='Visit https://github.com/tdpage/latex_tools for more info.')
        self.parser.add_argument('-o', '--output', default='new_document.tex',
                                 nargs='?', metavar='file',
                                 help='output file')
        self.parser.add_argument('-d', '--directory', default='new_document/',
                                 nargs='?', metavar='dir',
                                 help='output directory')
        self.parser.add_argument('-t', '--title', default='title',
                                 nargs='?', metavar='"doc title"',
                                 help='document title')
        self.parser.add_argument('-s', '--subtitle', default='subtitle',
                                 nargs='?', metavar='"doc subtitle"',
                                 help='document subtitle')
        self.parser.add_argument('-a', '--author', default=self.CUR_USR,
                                 nargs='?', metavar='"author name"',
                                 help='document author')
        self.parser.add_argument('-D', '--date', default=datetime.now().strftime('%d/%m/%Y'),
                                 nargs='?', metavar='MM/DD/YYYY',
                                 help='document date')
        self.parser.add_argument('-T', '--template', default='default',
                                 nargs='?', metavar='template',
                                 help='template to use')
        self.parser.add_argument('-c', '--compile', default=False,
                                 nargs='?', metavar='compiler',
                                 const="pdflatex",
                                 help='LaTeX compiler with args')
        
        # parse the args and place them as attributes of self
        self.parser.parse_args(namespace=self)
        
        self.default_template = r'''
% $TIMESTAMP

\documentclass{scrartcl}

\begin{document}
\author{$author}
\title{$title}
\subtitle{$subtitle}
\date{$date}

\maketitle

\end{document}

'''
        
    def make_folders(self):
        # todo: check if the directory is a relative or absolute path
        # todo: auto-append trailing / to directory if not present
        # todo?: check if the output file has .tex extension or not
        
        path = "./" + self.directory
        
        for subdir in ['circuit/', 'tex/', 'img/', 'table/']:
            try:
                os.makedirs(path + subdir)
            except:
                print('directory "' + path + subdir + '" already exists! skipping creation')
                        
    def load_template(self):
        # todo: allow changing templates
        # todo: read template from config dir
        
        if self.template == "default":
            self.file_contents = self.default_template
        
        else:
            path = os.path.expanduser('~/bin/latex_tools/templates/')
            try:
                with open(path + self.template + '.tex', 'r') as in_file:
                    self.file_contents = in_file.read()
            except:
                sys.stderr.write('cannot find "' + self.template + '" template!\n')
                sys.exit(1)
    
    def replace_contents(self):
        self.file_contents = self.file_contents.replace('$TIMESTAMP', self.TIMESTAMP)
        self.file_contents = self.file_contents.replace('$author', self.author)
        self.file_contents = self.file_contents.replace('$title', self.title)
        self.file_contents = self.file_contents.replace('$subtitle', self.subtitle)
        self.file_contents = self.file_contents.replace('$date', self.date)
    
    def write_file(self):
        path = "./" + self.directory
         
        try:
            with open(path  + self.output, 'w') as out_file:
                out_file.write(self.file_contents)
        except:
            sys.stderr('cannot open "' + path + '"')
            sys.exit(1)
            
    def compile_doc(self):
        # todo: verify safe execution of code
        # todo: exception handling
        
        # only compile if the flag was passed
        if self.compile:
            path = "./" + self.directory
            os.chdir(path)
            os.system(self.compile + " " + self.output)
            os.chdir('..')
            
def main():
    latex_obj = latexmakefolder()
    latex_obj.make_folders()
    latex_obj.load_template()
    latex_obj.replace_contents()
    latex_obj.write_file()
    latex_obj.compile_doc()
    


if __name__ == "__main__":
    main()
