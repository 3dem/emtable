# **************************************************************************
# *
# * Authors:  J. M. de la Rosa Trevin (delarosatrevin@gmail.com)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# **************************************************************************

import sys
from itertools import izip
from collections import OrderedDict, namedtuple
import copy


class Column:
    def __init__(self, name, type=None):
        self._name = name
        # Get the type from the LABELS dict, assume str by default
        self._type = type

    def __str__(self):
        return self._name

    def __cmp__(self, other):
        return self._name == str(other)


class Table:
    """
    Class to hold and manipulate tabular data for EM processing programs.
    """
    def __init__(self, **kwargs):
        self.clear()

        if 'fileName' in kwargs:
            if 'columns' in kwargs:
                raise Exception("Please provide either 'columns' or 'fileName',"
                                " but not both.")
            fileName = kwargs.get('fileName')
            tableName = kwargs.get('tableName', None)
            self.read(fileName, tableName)
        elif 'columns' in kwargs:
            self._createColums(kwargs['columns'])

    def clear(self):
        self.Row = None
        self._columns = OrderedDict()
        self._rows = []

    def _addColumn(self, nameOrTuple):
        """
        :param nameOrTuple: This parameter should be either a string or
            a tuple (string, type).
        """
        if isinstance(nameOrTuple, str):
            col = Column(nameOrTuple)
        elif isinstance(nameOrTuple, tuple):
            col = Column(nameOrTuple[0], nameOrTuple[1])
        else:
            raise Exception("Invalid input as column, "
                            "should be either string or tuple.")
        self._columns[str(col)] = col

    def _createColums(self, columnList):
        self.clear()
        for col in columnList:
            self._addColumn(col)
        self._createRowClass()

    def _createRowClass(self):
        self.Row = namedtuple('Row', [str(c) for c in self._columns])

    def _findDataLine(self, inputFile, dataStr):
        """ Raise an exception if the desired data string is not found.
        Move the line pointer after the desired line if found.
        """
        for line in inputFile:
            if line.startswith(dataStr):
                return line
        raise Exception("%s block was not found")

    def _findLabelLine(self, inputFile):
        for line in inputFile:
            if line.startswith('_'):
                return line
        return ''

    def addRow(self, *args, **kwargs):
        self._rows.append(self.Row(*args, **kwargs))

    def readStar(self, inputFile, tableName=None):
        """
        :param inputFile: Provide the input file from where to read the data.
            The file pointer will be moved until the last data line of the
            requested table.
        :return:
        """
        self.clear()
        dataStr = 'data_%s' % (tableName or '')
        print("dataStr:", dataStr)

        self._findDataLine(inputFile, dataStr)

        # Find first column line and parse all columns
        line = self._findLabelLine(inputFile)

        colNames = []
        while line.startswith('_'):
            colNames.append(line.split()[0].strip()[1:])
            line = inputFile.readline()

        self._createColums(colNames)

        line = line.strip()
        # Parse all data lines
        while line:
            self.addRow(*line.split())
            line = inputFile.readline().strip()

    def read(self, fileName, tableName=None):

        with open(fileName) as f:
            self.readStar(f, tableName)

    def writeStar(self, outputFile, tableName=None):
        outputFile.write("\ndata_%s\n\nloop_\n"
                         % (tableName or ''))
        line_format = ""

        for col in self._columns.values():
            outputFile.write("_%s \n" % col)

        for row in self._rows:
            outputFile.write(' '.join(row) + '\n')

        outputFile.write('\n')

    def write(self, output_star, tableName=None):
        with open(output_star, 'w') as output_file:
            self.writeStar(output_file, tableName)

    def printStar(self):
        self.writeStar(sys.stdout)

    def size(self):
        return len(self._data)

    def __len__(self):
        return self.size()

    def __iter__(self):
        for item in self._data:
            yield item

    def __getitem__(self, item):
        return self._rows[item]


