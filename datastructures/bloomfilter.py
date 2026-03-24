from typing import Any
import json
import random
import numpy as np
import hashlib

import matplotlib.pyplot as plt


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

if __name__ == '__oldmain__':

def run_over_exp_grid() -> list[list[int]]] :
    ns = [10, 10**2, 10**3, 10**4, 10**5, 10**6, 10**7, 10**8]
    mxcs = [2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12, 2**13, 2**14, 2**15]
    #ns = [10]
    collect_fprs = []
    for mxc in mxcs:
        for myn in ns:
            n = int(myn)
            bf = BloomFilter(mxc)
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
            print(f"{mxc=},{n=},{measured_fnr=}, {expected_fnr=}, {measured_fpr=}, {expected_fpr=},{fn=}, {p=}, {fp=}, {total_n=}, {len(bf.saved)=}")
            collect_fprs.append( [mxc, n, measured_fpr])
    return collect_fprs

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    data = [[16, 10, 0.2], [16, 100, 1.0], [16, 1000, 1.0], [16, 10000, 1.0], [16, 100000, 1.0], [16, 1000000, 1.0], [16, 10000000, 1.0], [16, 100000000, 1.0], [32, 10, 0.0], [32, 100, 1.0], [32, 1000, 1.0], [32, 10000, 1.0], [32, 100000, 1.0], [32, 1000000, 1.0], [32, 10000000, 1.0], [32, 100000000, 1.0], [64, 10, 0.0], [64, 100, 0.64], [64, 1000, 1.0], [64, 10000, 1.0], [64, 100000, 1.0], [64, 1000000, 1.0], [64, 10000000, 1.0], [64, 100000000, 1.0], [128, 10, 0.0], [128, 100, 0.34], [128, 1000, 1.0], [128, 10000, 1.0], [128, 100000, 1.0], [128, 1000000, 1.0], [128, 10000000, 1.0], [128, 100000000, 1.0], [256, 10, 0.0], [256, 100, 0.04], [256, 1000, 0.99], [256, 10000, 1.0], [256, 100000, 1.0], [256, 1000000, 1.0], [256, 10000000, 1.0], [256, 100000000, 1.0], [512, 10, 0.0], [512, 100, 0.02], [512, 1000, 0.882], [512, 10000, 1.0], [512, 100000, 1.0], [512, 1000000, 1.0], [512, 10000000, 1.0], [512, 100000000, 1.0], [1024, 10, 0.0], [1024, 100, 0.0], [1024, 1000, 0.444], [1024, 10000, 1.0], [1024, 100000, 1.0], [1024, 1000000, 1.0], [1024, 10000000, 1.0], [1024, 100000000, 1.0], [2048, 10, 0.0], [2048, 100, 0.0], [2048, 1000, 0.166], [2048, 10000, 0.9938], [2048, 100000, 1.0], [2048, 1000000, 1.0], [2048, 10000000, 1.0], [2048, 100000000, 1.0], [4096, 10, 0.0], [4096, 100, 0.0], [4096, 1000, 0.036], [4096, 10000, 0.9182], [4096, 100000, 1.0], [4096, 1000000, 1.0], [4096, 10000000, 1.0], [4096, 100000000, 1.0], [8192, 10, 0.0], [8192, 100, 0.0], [8192, 1000, 0.006], [8192, 10000, 0.5918], [8192, 100000, 1.0], [8192, 1000000, 1.0], [8192, 10000000, 1.0], [8192, 100000000, 1.0], [16384, 10, 0.0], [16384, 100, 0.0], [16384, 1000, 0.002], [16384, 10000, 0.2116], [16384, 100000, 0.99962], [16384, 1000000, 1.0], [16384, 10000000, 1.0], [16384, 100000000, 1.0], [32768, 10, 0.0], [32768, 100, 0.0], [32768, 1000, 0.0], [32768, 10000, 0.0538], [32768, 100000, 0.96818], [32768, 1000000, 1.0], [32768, 10000000, 1.0], [32768, 100000000, 1.0]]
    x = [row[0] for row in data]
    y = [row[1] for row in data]
    v = [row[2] for row in data]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    norm = mcolors.Normalize(vmin=0, vmax=1)
    
    sc = ax.scatter(x, y, c=v, cmap="viridis", norm=norm, s=80)

    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=10)

    for xi, yi, vi in zip(x, y, v):
        ax.annotate(
            f"{vi:.2f}",
            (xi, yi),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=9
        )

    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Value (0 to 1)")

    ax.set_xlabel("Capacity bits (log base 2)")
    ax.set_ylabel("N (log base 10)")
    ax.set_title("FPR -- false positive rate")

    plt.tight_layout()
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    plt.show()
    
