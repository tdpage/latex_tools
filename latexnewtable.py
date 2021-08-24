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


class latexnewtable():
    def __init__(self):
        
        # specify some meta information
        self.CUR_USR = pwd.getpwuid(os.getuid()).pw_name
        self.TIMESTAMP = datetime.now().strftime('%d/%m/%Y %I:%M %p') + ' by ' + self.CUR_USR
        
        self.file_contents = str()
        
        # set the arguments 
        self.parser = argparse.ArgumentParser(description='Add a new table .tex file to the LaTeX document.',
                                              epilog='Visit https://github.com/tdpage/latex_tools for more info.')
        self.parser.add_argument('-o', '--output', default='new_table.tex',
                                 nargs='?', metavar='file',
                                 help='output file')
        self.parser.add_argument('-d', '--directory', default='',
                                 nargs='?', metavar='dir',
                                 help='output directory')
        self.parser.add_argument('-c', '--caption', default=False,
                                 nargs='?', metavar='"table caption"',
                                 help='table caption')
        self.parser.add_argument('-t', '--toc', default=False,
                                 nargs='?', metavar='"TOC caption"',
                                 help='table of contents caption')
        self.parser.add_argument('-l', '--label', default=False,
                                 nargs='?', metavar='label',
                                 help='reference label')
        self.parser.add_argument('-u', '--update', action='store_true',
                                 help='update reflist.tex and floatlist.tex')
        # parse the args and place them as attributes of self
        self.parser.parse_args(namespace=self)
        
        docname = self.output.split('.')[0]
        if not self.label:
            self.label = docname
            
        if not self.caption:
            self.caption = docname
        
        if not self.toc:
            self.toc = self.caption
        
        self.file_contents = r'''% $TIMESTAMP
\begin{table}[!htbp]
    \centering
    \begin{tabular}{|c|c|}
        \hline
        Header 1 & Header 2 \\
        \hline
    \end{tabular}
    \caption[$toc_caption]{$caption}
    \label{tab:$label}
\end{table}
'''
    
    def replace_contents(self):
        self.file_contents = self.file_contents.replace('$TIMESTAMP', self.TIMESTAMP)
        self.file_contents = self.file_contents.replace('$caption', self.caption)
        self.file_contents = self.file_contents.replace('$toc_caption', self.toc)
        self.file_contents = self.file_contents.replace('$label', self.label)
    
    def write_file(self):
        
        # check if the table/ directory exists. If so, use that as a base
        if os.path.exists('./table/'):
            self.path = './table/' + self.directory
        else:
            self.path = './' + self.directory
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)
         
        try:
            with open(self.path  + self.output, 'w') as out_file:
                out_file.write(self.file_contents)
        except:
            print('cannot open "' + self.path + '"', file=sys.stderr)
            sys.exit(1)
            
    def update_lists(self):        
        # only compile if the flag was passed
        if self.update:
            try:
                with open('./listoffloats.tex', 'a') as out_file:
                    out_file.write(r'\input{'+ self.path + self.output + '}\n')
            except IOError:
                print('cannot open "' + path + '"', file=sys.stderr)
                sys.exit(1)
                
            try:
                with open('./listofrefs.tex', 'a') as out_file:
                    out_file.write(r'\ref{tab:'+ self.label + '}\n')
            except IOError:
                print('cannot open "' + path + '"', file=sys.stderr)
                sys.exit(1)
            
def main():
    latex_obj = latexnewtable()
    latex_obj.replace_contents()
    latex_obj.write_file()
    latex_obj.update_lists()
    


if __name__ == "__main__":
    main()
