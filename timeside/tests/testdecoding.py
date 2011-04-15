from timeside.core import *
from timeside.decoder import *
from timeside.api import *

from timeside.component import *
from timeside.tests import TestCase, TestRunner
import unittest

import os.path

__all__ = ['TestDecoding']

class TestLowLevel(TestCase):
    "Test the low level streaming features"

    def setUp(self):
        pass
   
    def testWav(self):
        "Test wav decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")

    def testFlac(self):
        "Test flac decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")

    def testOgg(self):
        "Test ogg decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")

    def testMp3(self):
        "Test mp3 decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")

    def tearDown(self):
        decoder = FileDecoder(self.source)
        decoder.setup()

        totalframes = 0.

        while True:
            frames, eod = decoder.process()
            totalframes += frames.shape[0]
            if eod: break

        # FIXME compute actual number of frames from file
        self.assertEquals(totalframes, 352801)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())


