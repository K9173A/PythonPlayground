# python3 only!

import os
import psutil

p = psutil.Process(os.getpid())

p.memory_info() # pmem(rss=15568896, vms=237490176, shared=8200192, text=8192, lib=0, data=7569408, dirty=0)
import sys
p.memory_info() # pmem(rss=17170432, vms=240320512, shared=8368128, text=8192, lib=0, data=9420800, dirty=0)

# https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_info
print((17170432 - 15568896) // 1024)
