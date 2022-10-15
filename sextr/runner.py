from os import system

from os import listdir, mkdir
from os.path import isfile, join

import time

TARGET_FOLDER = 'shared/processing_folder'
PROCESSED_FOLDER = 'shared/processed_folder'


def get_files_in_folder(folder):
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    return files

def run_sextractor():
    while True:
        time.sleep(0.2)
        to_process = get_files_in_folder(TARGET_FOLDER)

        for file in to_process:
            if not file.endswith(".fz"):
                continue
            
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
            if target_file.endswith(".fits"):
                code = system(f'sex {target_file} -c shared/config/config.sex -CATALOG_NAME {cat_name} -CHECKIMAGE_NAME {aper_name}')
                print(f'sextractor ran with code {code}.')
            
            system(f'rm {target_file}')

            


if __name__ == "__main__":
    try:
        run_sextractor()
    except KeyboardInterrupt as ex:
        print('shutdown!')