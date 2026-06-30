#     try:
# -*- coding: utf-8 -*-
import os
if False:

        import git  
        git.Git(".").clone("https://github.com/XLabs-AI/x-flux")
    except:
        
        os.system("git clone https://github.com/XLabs-AI/x-flux" )
 
cur_dir = os.path.dirname(os.path.abspath(__file__))
if False:
    run = f'mv x-flux "{cur_dir}/xflux"'
    if os.name == 'nt':
        run = f'move x-flux "{cur_dir}\\xflux"'
    os.system(run)
if os.name == 'nt':
    os.system(f'pip install -r "{cur_dir}\\requirements.txt"')
else:
    os.system(f'pip install -r "{cur_dir}/requirements.txt"')
print("Succesfully installed")
