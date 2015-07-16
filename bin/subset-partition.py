#!/usr/bin/env python
import time
import sys
sys.path.insert(1, 'python/')
import argparse
from subprocess import check_call, Popen, PIPE

parser = argparse.ArgumentParser()
parser.add_argument('--action', required=True)
args = parser.parse_args()

n_subsets = 10
for isub in range(n_subsets):
    cmd = './bin/compare-partition-methods.py --actions ' + args.action + ' --subset ' + str(isub) + ' --n-subsets ' + str(n_subsets)
    print cmd
    # Popen(cmd.split())
    check_call(cmd.split())
    # time.sleep(10)
    sys.exit()