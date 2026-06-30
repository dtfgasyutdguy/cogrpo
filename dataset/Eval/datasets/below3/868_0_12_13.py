# -*- coding: utf-8 -*-
import os
table = os.popen('squeue').read()
for line in str(table).split('\n'):
    
    if 'server.b' in line or 'batch.sh' in line:
        id = line.split('vip_gpu')[0] #change to your slurm partition name
        os.system(f'scancel {id}')

try:
    os.remove('./server.csv')

    pass
try:
# except:
    os.system('rm *.out')
except:
    pass
os.system('squeue')