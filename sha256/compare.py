#!/usr/bin/env python3

import sys
import colorama
import csv
from colorama import Fore, Style
from colorama import init, deinit
init()

jay = sys.argv[1]
tk4 = sys.argv[2]
stben = sys.argv[3]

jay_hash_to_path = {}
jay_hash_to_name = {}
jay_name_to_hash = {}
jay_path_to_hash = {}
tk4_hash_to_path = {}
tk4_name_to_hash = {}
tk4_path_to_hash = {}
tk4_hash_to_name = {}
stben_hash_to_path = {}
stben_name_to_hash = {}
stben_path_to_hash = {}
stben_hash_to_name = {}

with open(jay) as f:
	for x in f.readlines():
		name,path,hashed = x.strip('\n').split(',')
		jay_hash_to_path[hashed] = path 
		jay_name_to_hash[name] = hashed
		jay_path_to_hash[path] = hashed
		jay_hash_to_name[hashed] = name
		
with open(tk4) as f:
	for x in f.readlines():
		name,path,hashed = x.strip('\n').split(',')
		tk4_hash_to_path[hashed] = path 
		tk4_name_to_hash[name] = hashed 
		tk4_path_to_hash[path] = hashed
		tk4_hash_to_name[hashed] = name

with open(stben) as f:
	for x in f.readlines():
		name,path,hashed = x.strip('\n').split(',')
		stben_hash_to_path[hashed] = path 
		stben_name_to_hash[name] = hashed 
		stben_path_to_hash[path] = hashed
		stben_hash_to_name[hashed] = name

print("{}Comparing Jay to TK4 Sources{}".format(Fore.MAGENTA, Fore.GREEN))

missing_files = 0

only_in_jay = {}
for h in jay_hash_to_name:
	f = jay_hash_to_name[h]
	if h not in tk4_hash_to_path:
		#print("{} {} {}".format(Fore.RED,f, h))
		if f in tk4_name_to_hash:
			print("{}File Diff".format(Fore.CYAN))
			print("\t{}JAY: {} {}".format(Fore.GREEN, jay_hash_to_path[h],h))
			print("\t{}TK4: {} {}".format(Fore.RED,   tk4_hash_to_path[tk4_name_to_hash[f]],tk4_name_to_hash[f]))
		else:
			only_in_jay[f] = jay_hash_to_path[jay_name_to_hash[f]]
	else:	
		if f != tk4_hash_to_name[h]:
			print("{}File Name Mismatch:{}\n\tJAY: {} {}\n\tTK4: {} {}".format(
				Fore.CYAN,Fore.RED, 
				f, jay_hash_to_path[h],
				tk4_hash_to_name[h], tk4_hash_to_path[h]))

if len(only_in_jay) > 0:
	print("{}Only in JAY:".format(Fore.CYAN))
	for f in only_in_jay:
		print(Fore.RED,f,only_in_jay[f])

print("{}Comparing TK4 to JAY Sources{}".format(Fore.MAGENTA, Fore.GREEN))

missing_files = 0
only_in_tk4 = {}
for h in tk4_hash_to_name:
	f = tk4_hash_to_name[h]
	if h not in jay_hash_to_path:
		#print("{} {} {}".format(Fore.RED,f, h))
		if f in jay_name_to_hash:
			print("{}File Diff".format(Fore.CYAN))
			print("\t{}TK4: {} {}".format(Fore.GREEN, tk4_hash_to_path[h],h))
			print("\t{}JAY: {} {}".format(Fore.RED,   jay_hash_to_path[jay_name_to_hash[f]],jay_name_to_hash[f]))
		else:
			only_in_tk4[f] = tk4_hash_to_path[tk4_name_to_hash[f]]
	else:	
		#print(f)
		if f != jay_hash_to_name[h]:
			print("{}File Name Mismatch:{}\n\tTK4: {} {}\n\tJAY: {} {}".format(
				Fore.CYAN,Fore.RED, 
				f, tk4_hash_to_path[h],
				jay_hash_to_name[h], jay_hash_to_path[tk4_name_to_hash[f]]))


if len(only_in_tk4) > 0:
	print("{}Only in JAY:".format(Fore.CYAN))
	for f in only_in_tk4:
		print(Fore.RED,f,only_in_jay[f])

deinit()
