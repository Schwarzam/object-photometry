from os import system

from os import listdir, mkdir
from os.path import isfile, join

import pandas as pd
import time

from astropy.io import fits

from wrappersoperations import readWriteCats


ZPS = pd.read_csv('shared/config/iDR4_zero-points.csv')

TARGET_FOLDER = 'shared/processing_folder'
PROCESSED_FOLDER = 'shared/processed_folder'


def get_files_in_folder(folder):
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    return files

def get_detection_image(file):
    band = file.split("_")[3].replace(".fits.fz", "")

    data = None
    for filtr in ['G', 'Z', 'I', 'R']: 
        f = fits.open(join(TARGET_FOLDER, file.replace(f"_{band}", f"_{filtr}")))
        if data is None:
            data = f[1].data
        else:
            data += f[1].data
        
        if filtr == 'R':
            f[1].data = data
            f.writeto(join(TARGET_FOLDER, file.replace(f"_{band}", "_detection")), overwrite=True)
    
    detection_file = join(TARGET_FOLDER, file.replace(f"_{band}", "_detection"))
    system(f'funpack {detection_file}')
    system(f'rm {detection_file}')
    detection_file = detection_file.replace('.fz', '')
    return detection_file

def run_sextractor():
    while True:
        print('Wainting on main.py')
        time.sleep(0.2)
        to_process = get_files_in_folder(TARGET_FOLDER)
        print(to_process)
        detection_file = None
        
        if 'done' in to_process:
            system(f'rm {join(TARGET_FOLDER, "done")}')

            for file in to_process:
                if not file.endswith(".fz"):
                    continue

                if not detection_file:
                    try:
                        detection_file = get_detection_image(file)
                    except Exception as e: print(e)
                
                out_folder = f'{file.split("_")[0]}_{file.split("_")[1]}_{file.split("_")[2]}'
                band = file.split("_")[3].replace(".fits.fz", "")
                proc_folder = join(PROCESSED_FOLDER, out_folder)
                
                ra = float(file.split("_")[0])
                dec = float(file.split("_")[1])

                try: mkdir(proc_folder)
                except: pass
                try: mkdir(join(proc_folder, 'images'))
                except: pass
                try: mkdir(join(proc_folder, 'aper_images'))
                except: pass
                try: mkdir(join(proc_folder, 'catalogs'))
                except: pass

                target_file = join(TARGET_FOLDER, file)
                
                if file.endswith(".fz"):
                    system(f'funpack {target_file}')
                    system(f"mv {target_file} {join(proc_folder, 'images', file)}")
                    target_file = target_file.replace('.fz', '')
                
                cat_name = join(proc_folder, "catalogs", f"{band}.fits")
                aper_name = join(proc_folder, "aper_images", f"{band}.fits")
                
                # --- CHANGING SEXTRACTOR CONFIG ---
                sextR = readWriteCats()
                sextR.read_config('shared/config/config.sex')

                header = fits.getheader(target_file)

                sextR.config['SATUR_LEVEL']['value'] = header['SATURATE'] 
                sextR.config['GAIN']['value'] = header['GAIN']

                sextR.config['MAG_ZEROPOINT']['value'] = float(ZPS[ZPS['Field'] == header['OBJECT'].replace('_', '-')]['ZP_' + header['FILTER'].lower().replace('f', 'J0')])

                for i in header:
                    if 'FWHMSEXT' in i:
                        sextR.config['SEEING_FWHM']['value'] = header[i]

                sextR.write_file('shared/config/tmp.sex')
                # ------ // -------

                if target_file.endswith(".fits"):
                    code = system(f'sex {detection_file},{target_file} -c shared/config/tmp.sex -CATALOG_NAME {cat_name} -CHECKIMAGE_NAME {aper_name}')
                    print(f'sextractor ran with code {code}.')
                
                system(f'rm {target_file}')
                system(f'rm shared/config/tmp.sex')
            
            system(f'fpack {detection_file}')
            system(f'rm {detection_file}')
            detection_file = detection_file + '.fz'
            system(f"mv {detection_file} {join(proc_folder, 'images', 'detection_image.fits.fz')}")

            f = open(join(TARGET_FOLDER, f'sextr_done'), 'w')
            f.write(' ')
            f.close()
            
            

            


if __name__ == "__main__":
    try:
        run_sextractor()
    except KeyboardInterrupt as ex:
        print('shutdown!')