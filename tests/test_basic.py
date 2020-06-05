
import sys
import os
import psutil

try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
import unittest

from metadata import Table
from strings_star_relion import particles_3d_classify, one_micrograph_mc

here = os.path.abspath(os.path.dirname(__file__))


def testfile(*args):
    """ Return a given testfile. """
    return os.path.join(here, *args)


def memory_usage():
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem = process.memory_full_info().uss / float(1 << 20)
    print("Memory (MB):", mem)
    return mem


class TestTable(unittest.TestCase):
    """
    Our basic test class
    """
    def _checkColumns(self, table, columnNames):
        for colName, col in zip(columnNames, table.getColumns()):
            self.assertEqual(colName, col.getName())

    def test_read_particles(self):
        """
        Read from a particles .star file
        """
        t1 = Table()
        f1 = StringIO(particles_3d_classify)

        t1.readStar(f1)
        cols = t1.getColumns()

        self.assertEqual(len(t1), 16)
        self.assertEqual(len(cols), 25)

        # Check that all rlnEnabled is 1 and rlnMicrographId is increasing from 1 to 17
        for i, row in enumerate(t1):
            self.assertEqual(row.rlnEnabled, 1)
            self.assertEqual(int(row.rlnImageId), i + 1)

        f1.close()

    def test_read_blocks(self):
        """
        Read an star file with several blocks
        """
        t1 = Table()
        f1 = StringIO(one_micrograph_mc)

        # This is a single-row table (different text format key, value
        t1.readStar(f1, tableName='general')
        goldValues = [('rlnImageSizeX', '3710'),
                      ('rlnImageSizeY', '3838'),
                      ('rlnImageSizeZ', '19'),
                      ('rlnMicrographMovieName', 'Movies/14sep05c_00024sq_00003hl_00002es.frames.out.mrc'),
                      ('rlnMicrographBinning', '1.000000'),
                      ('rlnMicrographOriginalPixelSize', '0.980000'),
                      ('rlnMicrographDoseRate', '1.000000'),
                      ('rlnMicrographPreExposure', '0.000000'),
                      ('rlnVoltage', '300.000000'),
                      ('rlnMicrographStartFrame', '1'),
                      ('rlnMotionModelVersion', '1')
                      ]

        self._checkColumns(t1, [k for k, v in goldValues])
        row = t1[0]
        for k, v in goldValues:
            self.assertEqual(getattr(row, k), v)

        t1.readStar(f1, tableName='global_shift')
        cols = t1.getColumns()

        self.assertEqual(len(t1), 19)
        self._checkColumns(t1, ['rlnMicrographFrameNumber',
                                'rlnMicrographShiftX',
                                'rlnMicrographShiftY'])

        t1.readStar(f1, tableName='local_motion_model')

        self.assertEqual(len(t1), 36)
        self._checkColumns(t1, ['rlnMotionModelCoeffsIdx',
                                'rlnMotionModelCoeff'])
        coeffs = [int(v) for v in t1.getColumnValues('rlnMotionModelCoeffsIdx')]
        self.assertEqual(coeffs, list(range(36)))

        f1.close()

    def test_write_singleRow(self):
        t = Table()
        f1 = StringIO(one_micrograph_mc)
        t.readStar(f1, tableName='global_shift')
        t.writeStar(sys.stdout, tableName='global_shifts', singleRow=True)

        t = Table(columns=['rlnImageSizeX',
                           'rlnImageSizeY',
                           'rlnMicrographMovieName'])
        t.addRow(3710, 3838, 'Movies/14sep05c_00024sq_00003hl_00002es.frames.out.mrc')
        fn = '/tmp/test-single-row.star'
        with open(fn, 'w') as f:
            print("Writing star file to: ", fn)
            t.writeStar(f, singleRow=True)

    def test_iterRows(self):
        dataFile = testfile('star', 'multibody', 'relion_it017_data.star')
        table = Table(fileName=dataFile)

        # Let's open again the same file for iteration
        with open(dataFile) as f:
            tableReader = Table.Reader(f, tableName='Particles')

            for c1, c2 in zip(table.getColumns(), tableReader.getColumns()):
                self.assertEqual(c1, c2, "Column c1 (%s) differs from c2 (%s)"
                                 % (c1, c2))

                for r1, r2 in zip(table, tableReader):
                    self.assertEqual(r1, r2)

        # Now try directly with iterRows function
        for r1, r2 in zip(table,
                          Table.iterRows(dataFile, tableName='Particles')):
            self.assertEqual(r1, r2)

        defocusSorted = sorted(float(r.rlnDefocusU) for r in table)

        for d1, row in zip(defocusSorted,
                          Table.iterRows(dataFile,
                                         tableName='Particles',
                                         key=lambda r: r.rlnDefocusU)):
            self.assertAlmostEqual(d1, row.rlnDefocusU)

        # Test sorting by imageId column, also using getColumnValues and sort()
        imageIds = table.getColumnValues('rlnImageId')
        imageIds.sort()

        # Check sorted iteration give the total amount of rows
        rows = [r for r in Table.iterRows(dataFile,
                                          tableName='Particles',
                                          key='rlnImageId')]
        self.assertEqual(len(imageIds), len(rows))

        for id1, row in zip(imageIds,
                            Table.iterRows(dataFile,
                                           tableName='Particles',
                                           key='rlnImageId')):
            self.assertEqual(id1, row.rlnImageId)

        def getIter():
            """ Test a function to get an iterator. """
            return Table.iterRows(dataFile,
                                  tableName='Particles', key='rlnImageId')

        iterByIds = getIter()
        for id1, row in zip(imageIds, iterByIds):
            self.assertEqual(id1, row.rlnImageId)

    def test_removeColumns(self):
        dataFile = testfile('star', 'multibody', 'relion_it017_data.star')
        table = Table(fileName=dataFile)
        
        expectedCols = [
            'rlnEnabled',
            'rlnCoordinateX',
            'rlnCoordinateY',
            'rlnMicrographName',
            'rlnMicrographId',
            'rlnImageId',
            'rlnImageName',
            'rlnDefocusU',
            'rlnDefocusV',
            'rlnDefocusAngle',
            'rlnAmplitudeContrast',
            'rlnSphericalAberration',
            'rlnVoltage',
            'rlnDetectorPixelSize',
            'rlnRandomSubset',
            'rlnBeamTiltX',
            'rlnBeamTiltY',
            'rlnGroupName',
            'rlnGroupNumber',
            'rlnAngleRot',
            'rlnAngleTilt',
            'rlnAnglePsi',
            'rlnOriginX',
            'rlnOriginY',
            'rlnClassNumber',
            'rlnNormCorrection',
            'rlnLogLikeliContribution',
            'rlnMaxValueProbDistribution',
            'rlnNrOfSignificantSamples'
        ]

        colsToRemove = [
            'rlnMicrographName',
            'rlnMicrographId',
            'rlnImageId',
            'rlnImageName',
            'rlnAmplitudeContrast',
            'rlnSphericalAberration',
            'rlnVoltage',
            'rlnDetectorPixelSize',
            'rlnRandomSubset',
            'rlnAngleRot',
            'rlnAngleTilt',
            'rlnAnglePsi',
            'rlnOriginX',
            'rlnOriginY',
            'rlnLogLikeliContribution',
            'rlnMaxValueProbDistribution',
            'rlnNrOfSignificantSamples'
        ]

        # Check all columns were read properly
        self.assertEqual(expectedCols, table.getColumnNames())
        # Check also using hasAllColumns method
        self.assertTrue(table.hasAllColumns(expectedCols))

        table.removeColumns(colsToRemove)
        self.assertEqual([c for c in expectedCols if c not in colsToRemove],
                         table.getColumnNames())
        # Check also using hasAnyColumn method
        self.assertFalse(table.hasAnyColumn(colsToRemove))

    def test_addColumns(self):
        dataFile = testfile('star', 'multibody', 'relion_it017_sampling.star')
        table = Table(fileName=dataFile, tableName='sampling_directions')

        expectedCols = ['rlnAngleRot',
                        'rlnAngleTilt',
                        'rlnAnglePsi',
                        'rlnExtraAngle1',
                        'rlnExtraAngle2',
                        'rlnAnotherConst'
                        ]

        self.assertEqual(expectedCols[:2], table.getColumnNames())

        table.addColumns('rlnAnglePsi=0.0',
                         'rlnExtraAngle1=rlnAngleRot',
                         'rlnExtraAngle2=rlnExtraAngle1',
                         'rlnAnotherConst=1000')

        self.assertEqual(expectedCols, table.getColumnNames())

        # Check values
        def _values(colName):
            return table.getColumnValues(colName)

        for v1, v2, v3 in zip(_values('rlnAngleRot'),
                              _values('rlnExtraAngle1'),
                              _values('rlnExtraAngle2')):
            self.assertAlmostEqual(v1, v2)
            self.assertAlmostEqual(v1, v3)

        self.assertTrue(all(v == 1000 for v in _values('rlnAnotherConst')))

        tmpOutput = '/tmp/sampling.star'
        print("Writing to: ", tmpOutput)
        table.write(tmpOutput, tableName='sampling_directions')


N = 100


def read_metadata():
    dataFile = testfile('star', 'multibody', 'relion_it017_sampling.star')
    tables = []
    for i in range(N):
        tables.append(Table(fileName=dataFile,
                            tableName='sampling_directions'))
    memory_usage()


def read_emcore():
    import emcore as emc
    dataFile = testfile('star', 'multibody', 'relion_it017_sampling.star')
    tables = []
    for i in range(N):
        t = emc.Table()
        t.read('sampling_directions', dataFile)
        tables.append(t)
    memory_usage()


if __name__ == '__main__':
    unittest.main()
    #read_metadata()
    #read_emcore()

