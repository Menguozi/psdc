#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
from simhash import Simhash

# 指定要遍历的目录
print(sys.argv[1])
rootdir = sys.argv[1]
total_file_count = 0
total_dir_count = 0
all_file_size = []
all_small_file = []

# 遍历目录及其子目录
for subdir, dirs, files in os.walk(rootdir,followlinks=False):
    for file in files:
        # 打印文件名
        is_file = os.path.isfile(os.path.join(subdir, file))
        if(is_file):
            file_size = os.path.getsize(os.path.join(subdir, file))
            if(file_size > 4096):
                # print(os.path.join(subdir, file))
                # print(file_size)
                all_file_size.append(file_size)
                all_small_file.append(os.path.join(subdir, file))
                total_file_count = total_file_count + 1
    for dir in dirs:
        # 打印目录名
        total_dir_count = total_dir_count + 1
        # print(os.path.join(subdir, dir))

print("total_file_count:", total_file_count)
print("total_dir_count:", total_dir_count)
print("average_file_size:", sum(all_file_size)/len(all_file_size))

all_simhash = []

def cal_simhash():
    for path in all_small_file:
        with open(path, encoding='ISO-8859-1') as file:
            content = file.read()
            all_simhash.append(Simhash(content))

cal_simhash()

file_simhash = open("small_file_simhash_sin.txt", "w+")
for i in range(len(all_simhash)):
    file_simhash.write(str(all_simhash[i].value))
    file_simhash.write("\n")
    print(all_simhash[i].value)
file_simhash.close()
