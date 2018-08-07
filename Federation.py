#!/usr/bin/env python3
import os
import random
import sys
import time
import shutil
import json
import util
from MultiSig import MultiSig
from BlockSigning import BlockSigning
from test_framework.authproxy import AuthServiceProxy, JSONRPCException

ELEMENTS_PATH = "../../../src/elementsd"
GENERATE_KEYS = False
BLOCK_TIME = 60

def main():
    # GENERATE KEYS AND SINGBLOCK SCRIPT FOR FEDERATION BLOCK SIGNING
    num_of_nodes = 3
    num_of_sigs = 2
    keys = []
    signblockarg = ""

    if GENERATE_KEYS:  # generate new signing keys and multisig
        if num_of_sigs > num_of_nodes:
                raise ValueError("Num of sigs cannot be larger than num of nodes")
        sig = MultiSig(num_of_nodes, num_of_sigs)
        keys = sig.wifs
        signblockarg = "-signblockscript={}".format(sig.script)
        with open('federation_data.json', 'w') as data_file:
            data = {"keys" : keys, "signblockarg" : signblockarg}
            json.dump(data, data_file)

    else:   # use hardcoded keys and multisig
        with open('federation_data.json') as data_file:
            data = json.load(data_file)
        keys = data["keys"]
        signblockarg = data["signblockarg"]

    # INIT ELEMENTS FEDERATION NODES
    elements_nodes = []
    tmpdir="/tmp/"+''.join(random.choice('0123456789ABCDEF') for i in range(5))
    for i in range(0, num_of_nodes):
        datadir = tmpdir + "/node" + str(i)
        os.makedirs(datadir)

        confdir="node"+str(i)+"/elements.conf"
        shutil.copyfile(confdir, datadir+"/elements.conf")
        mainconf = util.loadConfig(confdir)

        print("Starting node {} with datadir {} and confdir {}".format(i, datadir, confdir))
        e = util.startelementsd(ELEMENTS_PATH, datadir, mainconf, signblockarg)
        time.sleep(5)
        elements_nodes.append(e)
        e.importprivkey(keys[i])
        time.sleep(2)

    # INIT BLOCK SIGNING
    node_signers = []
    for i in range(num_of_nodes):
        node = BlockSigning(i, elements_nodes[i], num_of_nodes, BLOCK_TIME)
        node_signers.append(node)
        node.start()

    try:
        while 1:
            time.sleep(300)

    except KeyboardInterrupt:
        for node in node_signers:
            node.stop()

        for elements in elements_nodes:
            elements.stop()

        shutil.rmtree(tmpdir)

if __name__ == "__main__":
    main()
