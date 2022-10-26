import splusdata
import os
import pandas as pd
import time

conn = splusdata.connect()

bands = ['R', 'G', 'I', 'U', 'Z', 'F378', 'F395', 'F410', 'F430', 'F515', 'F660', 'F861']
processing_folder = 'sextr/shared/processing_folder/'

WAIT_TIME = 10

def insert_table():
    print(" -- insert table path -- ")
    path = input("table path: ")
    
    df = pd.read_csv(path.strip())
    if 'size' not in df.columns:
        size = input('size: ')

    for key, value in df.iterrows():
        for band in bands:
            ra = value['RA']
            dec = value['DEC']
            if 'size' in df.columns:
                size = value['size']

            cut = conn.get_cut(ra, dec, size, band)
            cut.writeto(os.path.join(processing_folder, f'{ra}_{dec}_{size}_{band}.fits.fz'), overwrite=True)
            print(f"downloaded {ra} {dec} {size} {band}")
        
        print(f"Wainting to sextractor to finish for {WAIT_TIME}")
        time.sleep(WAIT_TIME)
        if 'ID' in df.columns:
            os.system(f"python3 join_tables.py {ra}_{dec}_{size} {value['ID'].strip()}")
        else:
            os.system(f"python3 join_tables.py {ra}_{dec}_{size}")
            
def insert_manual():
    print(" -- new object -- ")
    ra = input("RA: ").strip()
    dec = input("DEC: ").strip()

    size = input('size: ')
    
    for band in bands:
        cut = conn.get_cut(ra, dec, size, band)
        cut.writeto(os.path.join(processing_folder, f'{ra}_{dec}_{size}_{band}.fits.fz'), overwrite=True)
        print(f"downloaded {ra} {dec} {size} {band}")
    
    print(f"Wainting to sextractor to finish for {WAIT_TIME}")
    time.sleep(WAIT_TIME)
    os.system(f"python3 join_tables.py {ra}_{dec}_{size}")
    print("")

while True:
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
    
    
