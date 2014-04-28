#! /usr/bin/env python

from unit_timeside import *
from timeside.decoder.file import FileDecoder
from timeside.analyzer import WITH_AUBIO
if WITH_AUBIO:
    from timeside.analyzer.aubio_pitch import AubioPitch
import os


@unittest.skipIf(not WITH_AUBIO, 'Aubio library is not available')
class TestAubioPitch(unittest.TestCase):

    def setUp(self):
        self.analyzer = AubioPitch()

    def testOnSweep(self):
        "runs on sweep"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "sweep.wav")

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        #print "result:", self.analyzer.result()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
