# Author: Gustavo Schwarz - gustavo.b.schwarz@gmail.com
# This script was written to the S-PLUS community.

import splusdata
import os
import pandas as pd
import time

from os import listdir, mkdir
from os.path import isfile, join


conn = splusdata.connect()

bands = ['R', 'G', 'I', 'U', 'Z', 'F378', 'F395', 'F410', 'F430', 'F515', 'F660', 'F861']
processing_folder = 'sextr/shared/processing_folder/'
processed_folder = 'sextr/shared/processed_folder/'

# If you want to keep the final catalogs, images and aper folders, change the values below to True
KEEP_FINAL_CATALOGS = True
KEEP_FINAL_IMAGES = True
KEEP_FINAL_APER = True

def get_files_in_folder(folder):
    """Get all files in a folder"""
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    return files

def wait_sextr():
    """Wait for sextractor to finish"""
    while True:
        time.sleep(0.2)
        files = get_files_in_folder(processing_folder)
        if 'sextr_done' in files:
            os.system(f'rm {join(processing_folder, "sextr_done")}')
        
            break

def clear_processing():
    """Clears processing folder"""
    files = get_files_in_folder(processing_folder)
    for file in files:
        os.system(f'rm {join(processing_folder, file)}')

def insert_table():
    print(" -- insert table path -- ")
    path = input("table path: ")
    
    df = pd.read_csv(path.strip())
    if 'size' not in df.columns:
        size = input('size: ')

    for key, value in df.iterrows():
        try:
            for band in bands:
                ra = value['RA']
                dec = value['DEC']
                if 'size' in df.columns:
                    size = value['size']

                cut = conn.get_cut(ra, dec, size, band)
                cut.writeto(os.path.join(processing_folder, f'{ra}_{dec}_{size}_{band}.fits.fz'), overwrite=True)
                print(f"downloaded {ra} {dec} {size} {band}")
                
        except Exception as e:
            print(e)
            clear_processing()
            print(f"Error on {ra} {dec}")
            continue
        
        f = open(os.path.join(processing_folder, f'done'), 'w')
        f.write(' ')
        f.close()

        print(f"Wainting to sextractor to finish.")
        wait_sextr()
        os.system(f"python3 join_tables.py {ra}_{dec}_{size}")

        if not KEEP_FINAL_CATALOGS:
            os.system(f'rm -rf {join(processed_folder, f"{ra}_{dec}_{size}", "catalogs")}')
        if not KEEP_FINAL_IMAGES:
            os.system(f'rm -rf {join(processed_folder, f"{ra}_{dec}_{size}", "images")}')
        if not KEEP_FINAL_APER: 
            os.system(f'rm -rf {join(processed_folder, f"{ra}_{dec}_{size}", "aper")}')

            
def insert_manual():
    print(" -- new object -- ")
    ra = input("RA: ").strip()
    dec = input("DEC: ").strip()

    size = input('size: ')
    
    for band in bands:
        cut = conn.get_cut(ra, dec, size, band)
        cut.writeto(os.path.join(processing_folder, f'{ra}_{dec}_{size}_{band}.fits.fz'), overwrite=True)
        print(f"downloaded {ra} {dec} {size} {band}")
    
    f = open(os.path.join(processing_folder, f'done'), 'w')
    f.write(' ')
    f.close()
    
    print(f"Waiting to sextractor to finish")
    wait_sextr()

    os.system(f"python3 join_tables.py {ra}_{dec}_{size}")

    if not KEEP_FINAL_CATALOGS:
        os.system(f'rm -rf {join(processed_folder, f"{ra}_{dec}_{size}", "catalogs")}')
    if not KEEP_FINAL_IMAGES:
        os.system(f'rm -rf {join(processed_folder, f"{ra}_{dec}_{size}", "images")}')
    if not KEEP_FINAL_APER: 
        os.system(f'rm -rf {join(processed_folder, f"{ra}_{dec}_{size}", "aper")}')

    print("")

while True:
    clear_processing()
    opt = input("""
    1 - Insert one object.
    2 - Insert table. 
    -- Table must have ID, RA, DEC columns
    -- You may also add a 'size' column if wanted.
    """)

    if opt.strip() == "1":
        insert_manual()
    if opt.strip() == "2":
        insert_table()
    
    
