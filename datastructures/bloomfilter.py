from typing import Any
import json
import random
import numpy as np
import hashlib

class BloomFilter:
    def __init__(self, max_capacity=128):
        self.bit_field = [False]* max_capacity
        self.maxc = max_capacity
        self.saved = {}
    def fast_has_item(self, key: Any):
        data = json.dumps(key, sort_keys=True).encode('utf-8')
        h1 = int(hashlib.sha3_224(data).hexdigest()[-4:], 16)
        h2 = int(hashlib.sha3_256(data).hexdigest()[-4:], 16)
        h3 = int(hashlib.sha3_384(data).hexdigest()[-4:], 16)
        #print(f"In fast has item: {key=},{h1=}, {h2=}, {h3=} ")

        if self.bit_field[h1 % self.maxc] and self.bit_field[h2 % self.maxc] and self.bit_field[h3 % self.maxc]:
            return True
        return False

    def has_item(self, key: Any):
        data = json.dumps(key, sort_keys=True).encode('utf-8')        
        if data in self.saved:
            return True
        return False
    def add(self, key: Any, item: Any):
        data = json.dumps(key, sort_keys=True).encode('utf-8')
        self.saved[data] = item        
        h1 = int(hashlib.sha3_224(data).hexdigest()[-4:], 16)
        h2 = int(hashlib.sha3_256(data).hexdigest()[-4:], 16)
        h3 = int(hashlib.sha3_384(data).hexdigest()[-4:], 16)

        self.bit_field[h1 % self.maxc] = True
        self.bit_field[h2 % self.maxc] = True
        self.bit_field[h3 % self.maxc] = True
        #print(f"In add: {key=},{h1=}, {h2=}, {h3=}, {self.bit_field=} ")        

if __name__ == '__main__':

    ns = [10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9]
    #ns = [10]
    for myn in ns:
        n = int(myn)
        bf = BloomFilter()        
        print(f"Creating {n} kvs")
        its = np.random.random(n)
        halfn = len(its) // 2
        for i in range(halfn):
            bf.add(its[i],its[i])
        #print(f"{bf.saved=}")
        fnr = 0
        fn = 0
        p = 0
        for i in range(halfn):
            if not bf.fast_has_item(its[i]) and bf.has_item(its[i]):
                fn = fn + 1
            if bf.has_item(its[i]):
                p = p + 1
        print("-"*10)
        measured_fnr = fn / p
        expected_fnr = fn / halfn
        fp = 0
        total_n = 0
        for i in range(halfn, n):
            if bf.fast_has_item(its[i]) and not bf.has_item(its[i]):
                fp = fp + 1
            if not bf.has_item(its[i]):
                total_n = total_n + 1
        measured_fpr = fp / total_n
        expected_fpr = fp / (n - halfn)
        print(f"{n=},{measured_fnr=}, {expected_fnr=}, {measured_fpr=}, {expected_fpr=},{fn=}, {p=}, {fp=}, {total_n=}, {len(bf.saved)=}")
