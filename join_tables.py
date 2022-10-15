from astropy.table import Table, vstack


from os import system

from os import listdir, mkdir
from os.path import isfile, join

import numpy as np
from astropy import wcs
from astropy import coordinates as coord
from astropy import units as u


folder = 'sextr/shared/processed_folder'

bands = ['R', 'G', 'I', 'U', 'Z', 'F378', 'F395', 'F410', 'F430', 'F515', 'F660', 'F861']

def match(t, ra, dec):
    ra2 = np.array(t['ALPHA_J2000'])
    dec2 = np.array(t['DELTA_J2000'])
    c = coord.SkyCoord(ra=ra, dec=dec, unit=(u.degree, u.degree))
    catalog = coord.SkyCoord(ra=ra2, dec=dec2, unit=(u.degree, u.degree))
    idx, d2d, d3d = c.match_to_catalog_sky(catalog)
    return idx, d2d, d3d

def get_files_in_folder(folder):
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    return files

def main():
    folder_name = input('folder name (Ex: RA_DEC_size): ')
    target_folder = join(folder, folder_name, 'catalogs')
    files = get_files_in_folder(target_folder)

    ra = float(folder_name.split("_")[0])
    dec = float(folder_name.split("_")[1])

    if len(files) < 1:
        print('No files found')

    tabs = {}
    for file in files:
        band = file.replace('.fits', '')
        tabs[band] = Table.read(join(target_folder, file))
            
        if len(tabs[band]) > 0:
            idx, d2d, _ = match(tabs[band], ra, dec)
            if d2d > 1 * u.deg:
                print(f'No object found on band {band}')
                continue

            tabs[band] = tabs[band][tabs[band]['NUMBER'] == tabs[band][idx]['NUMBER']]
        tabs[band]['FILTER'] = band

    stack = []
    for tab in tabs:
        stack.append(tabs[tab])
    
    res = vstack(stack)
    res.write(join(folder, folder_name, 'final_table.fits'))

    print('Done!')
if __name__ == '__main__':
    main()