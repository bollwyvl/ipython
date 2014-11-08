"""restructuredText Exporter class"""

#-----------------------------------------------------------------------------
# Copyright (c) 2013, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import re

from IPython.config import Config
from IPython.nbformat import v4

from .importer import Importer

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------


is_indented_code = re.compile(r'^(\s{4,})\S')
is_fenced_code = re.compile(r'[~`]{3,}(?P<lang>[^~`]*?)\n?$')

is_doctest_start = re.compile(r'^>>> ')
is_doctest_cont = re.compile(r'^\.\.\. ')


class MarkdownImporter(Importer):
    """
    Imports markdown text documents.
    """

    def to_notebook_node(self, contents, resources=None, **kw):
        """
        convert a unicode markdown document into a notebook node

        Parameters
        ----------
        contents : unicode
            the string of markdown
        resources : dict
            don't know yet
        """
        nb = v4.new_notebook()

        nb.cells = list(self.parse(contents.splitlines(True)))

        return nb, resources

    def make_cells(self, cell_type, source, cell_magic=None):
        """
        Make some cells of a type from some source
        
        Parameters
        ----------
        cell_type : function
            the factory function for new cells
        source : list
            lines of source
        """
        if source is not None:
            if cell_type is v4.new_code_cell and source:
                source = self.strip_last(self.dedent(source))
                
                if cell_magic and cell_magic != "python":
                    cell_magic = "%%{0}\n".format(cell_magic)
                
                if is_doctest_start.match(source[0]):
                    for cell in self.doctestify(cell_type,
                                                source,
                                                cell_magic=cell_magic):
                        yield cell
                else:
                    yield cell_type(source=source)
            else:
                yield cell_type(source=source)

    def strip_last(self, source):
        if source:
            source[-1] = source[-1].rstrip()
        return source

    def dedent(self, source):
        """
        Reduce multiple source lines' indentation by the amount of the
        first line's indentation.
        
        Parameters
        ----------
        source : list
            lines of source
        """
        indented = is_indented_code.match(source[0])
        if indented:
            indent = len(indented.groups()[0])
            source = [line[indent:] for line in source]
        return source
    
    def doctestify(self, cell_type, source, cell_magic=None):
        """
        Find and emit doctest cells... will have to have started with a doctest
        
        Parameters
        ----------
        cell_type : function
            factory for cell type... it's probably make_new_code_cell
        source : list
            lines of source... and output?
        cell_magic : string
            a magic to insert in front of each input
        """
        
        cell_magic = [cell_magic] if cell_magic else [] 
        
        doc_input = []
        doc_output = []
        
        def _make_cell():
            return cell_type(
                source=self.strip_last(cell_magic + doc_input),
                outputs=[v4.new_output(
                    "execute_result",
                    data={"text/plain": self.strip_last(doc_output)},
                    execution_count=0
                )]
            )
        
        for line in source:
            if is_doctest_start.match(line):
                if doc_input:
                    yield _make_cell()
                    doc_input, doc_output = [], []
                
                doc_input += [line[4:]]
            elif is_doctest_cont.match(line):
                doc_input += [line[4:]]
            else:
                doc_output += [line]
        
        if doc_input:
            yield _make_cell()

    def parse(self, lines):
        """
        Break a markdown document (as lines of text) into discrete cells
        
        Parameters
        ----------
        source : list
            lines of source
        """
        
        source = None
        cell_type = None
        fenced = False
        lang = None

        for line in lines:
            if is_indented_code.match(line):
                if cell_type == v4.new_code_cell:
                    source += [line]
                else:
                    for cell in self.make_cells(cell_type, source): yield cell
                    cell_type, source = v4.new_code_cell, [line]
            elif is_fenced_code.match(line):
                # start or end a fenced cell line
                if not fenced:
                    for cell in self.make_cells(cell_type, source): yield cell
                    fenced = True
                    match = is_fenced_code.match(line).groupdict()
                    lang = match["lang"]
                    
                    cell_type, source = v4.new_code_cell, []
                else:
                    for cell in self.make_cells(cell_type, source, cell_magic=lang): yield cell
                    cell_type, source, lang = None, None, None
                    fenced = False
            elif fenced:
                # continue a fenced line
                source += [line]
            else:
                # just some stuff
                if cell_type == v4.new_markdown_cell:
                    source += [line]
                else:
                    for cell in self.make_cells(cell_type, source): yield cell
                    cell_type, source = v4.new_markdown_cell, [line]
        # cleanup
        for cell in self.make_cells(cell_type, source): yield cell
