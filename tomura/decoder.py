#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import zlib

class DeflateDecoder(object):

    def __init__(self):
        self._first_try = True
        self._data = bytes()
        self._obj = zlib.decompressobj()

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def decompress(self, data):
        if not data:
            return data

        if not self._first_try:
            return self._obj.decompress(data)

        self._data += data
        try:
            decompressed = self._obj.decompress(data)
            if decompressed:
                self._first_try = False
                self._data = None
            return decompressed
        except zlib.error:
            self._first_try = False
            self._obj = zlib.decompressobj(-zlib.MAX_WBITS)
            try:
                return self.decompress(self._data)
            finally:
                self._data = None


class GzipDecoderState(object):

    FIRST_MEMBER = 0
    OTHER_MEMBERS = 1
    SWALLOW_DATA = 2


class GzipDecoder(object):

    def __init__(self):
        self._obj = zlib.decompressobj(16 + zlib.MAX_WBITS)
        self._state = GzipDecoderState.FIRST_MEMBER

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def decompress(self, data):
        ret = bytes()
        if self._state == GzipDecoderState.SWALLOW_DATA or not data:
            return ret
        while True:
            try:
                ret += self._obj.decompress(data)
            except zlib.error:
                previous_state = self._state
                # Ignore data after the first error
                self._state = GzipDecoderState.SWALLOW_DATA
                if previous_state == GzipDecoderState.OTHER_MEMBERS:
                    # Allow trailing garbage acceptable in other gzip clients
                    return ret
                raise
            data = self._obj.unused_data
            if not data:
                return ret
            self._state = GzipDecoderState.OTHER_MEMBERS
            self._obj = zlib.decompressobj(16 + zlib.MAX_WBITS)

def get_decoder(mode):
    if mode == 'gzip':
        return GzipDecoder()

    return DeflateDecoder()
