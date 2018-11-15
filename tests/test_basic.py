
import sys
from cStringIO import StringIO
import unittest

from metadata import Table
from strings_star_relion import particles_3d_classify, one_micrograph_mc


class TestTable(unittest.TestCase):
    """
    Our basic test class
    """
    def _checkColumns(self, table, columnNames):
        for colName, col in zip(columnNames, table.getColumns()):
            self.assertEqual(colName, str(col))

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
            self.assertEqual(row.rlnEnabled, '1')
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
        self.assertEqual(coeffs, range(36))

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


if __name__ == '__main__':
    unittest.main()

