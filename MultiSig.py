#!/usr/bin/env python3
import codecs
import hashlib
from test_framework import (
    address,
    key,
    util,
)
from util import *

class MultiSig():
    def __init__(self, nodes, sigs):
        self.num_of_nodes = nodes
        self.num_of_sigs = sigs
        self.keys = []
        self.wifs = []
        self.script = ""
        self.initKeys()
        self.generate()

    def initKeys(self):
        for i in range(self.num_of_nodes):
            k = key.CECKey()
            pk_bytes = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).digest()
            k.set_secretbytes(pk_bytes)
            self.keys.append(k)
            self.wifs.append(address.byte_to_base58(pk_bytes, 239))

    def generate(self):
        script = "{}".format(50 + self.num_of_sigs)
        for i in range(self.num_of_nodes):
            k = self.keys[i]
            script += "41"
            script += codecs.encode(k.get_pubkey(), 'hex_codec').decode("utf-8")
        script += "{}".format(50 + self.num_of_nodes) # num keys
        script += "ae" # OP_CHECKMULTISIG
        print('signblockscript', script)
        self.script = script
