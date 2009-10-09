# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Guillaume Pellerin <yomguy@parisson.com>

import os
import string
import subprocess

from timeside.encode.core import *
from timeside.encode.api import IEncoder


class Mp3Encoder(EncoderCore):
    """Defines methods to encode to MP3"""

    implements(IEncoder)

    def __init__(self):
        self.description = self.description()
        self.format = self.format()
        self.mime_type = self.mime_type()
        self.bitrate_default = '192'
        self.dub2id3_dict = {'title': 'TIT2', #title2
                             'creator': 'TCOM', #composer
                             'creator': 'TPE1', #lead
                             'identifier': 'UFID', #Unique ID...
                             'identifier': 'TALB', #album
                             'type': 'TCON', #genre
                             'publisher': 'TPUB', #comment
                             #'date': 'TYER', #year
                             }
        self.dub2args_dict = {'title': 'tt', #title2
                             'creator': 'ta', #composerS
                             'relation': 'tl', #album
                             #'type': 'tg', #genre
                             'publisher': 'tc', #comment
                             'date': 'ty', #year
                             }
    def get_format(self):
        return 'MP3'

    def get_file_extension(self):
        return 'mp3'

    def get_mime_type(self):
        return 'audio/mpeg'

    def get_description(self):
        return """
        MPEG-1 Audio Layer 3, more commonly referred to as MP3, is a patented
        digital audio encoding format using a form of lossy data compression.
        It is a common audio format for consumer audio storage, as well as a
        de facto standard of digital audio compression for the transfer and
        playback of music on digital audio players. MP3 is an audio-specific
        format that was designed by the Moving Picture Experts Group as part
        of its MPEG-1 standard. (source Wikipedia)
        """

    def get_file_info(self):
        try:
            file_out1, file_out2 = os.popen4('mp3info "'+self.dest+'"')
            info = []
            for line in file_out2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('EncoderError: file does not exist.')

    def write_tags(self):
        """Write all ID3v2.4 tags by mapping dub2id3_dict dictionnary with the
            respect of mutagen classes and methods"""
        from mutagen import id3
        id3 = id3.ID3(self.dest)
        for tag in self.metadata.keys():
            if tag in self.dub2id3_dict.keys():
                frame_text = self.dub2id3_dict[tag]
                value = self.metadata[tag]
                frame = mutagen.id3.Frames[frame_text](3,value)
                try:
                    id3.add(frame)
                except:
                    raise IOError('EncoderError: cannot tag "'+tag+'"')
        try:
            id3.save()
        except:
            raise IOError('EncoderError: cannot write tags')

    def get_args(self):
        """Get process options and return arguments for the encoder"""
        args = []
        if not self.options is None:
            if not ( 'verbose' in self.options and self.options['verbose'] != '0' ):
                args.append('-S')
            if 'mp3_bitrate' in self.options:
                args.append('-b ' + self.options['mp3_bitrate'])
            else:
                args.append('-b '+self.bitrate_default)
            #Copyrights, etc..
            args.append('-c -o')
        else:
            args.append('-S -c -o')

        for tag in self.metadata:
            name = tag[0]
            value = clean_word(tag[1])
            if name in self.dub2args_dict.keys():
                arg = self.dub2args_dict[name]
                args.append('--' + arg + ' "' + value + '"')
        return args

    def process(self, source, metadata, options=None):
        self.metadata = metadata
        self.options = options
        args = get_args(options)
        args = ' '.join(args)
        command = 'lame %s - -' % args

        stream = self.core_process(command, source)
        for __chunk in stream:
            yield __chunk
