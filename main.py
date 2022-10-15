import splusdata
import os

conn = splusdata.connect()

bands = ['R', 'G', 'I', 'U', 'Z', 'F378', 'F395', 'F410', 'F430', 'F515', 'F660', 'F861']
processing_folder = 'sextr/shared/processing_folder'

while True:
    print(" -- new object -- ")
    ra = input("RA: ").strip()
    dec = input("DEC: ").strip()

    size = input('size: ')

    for band in bands:
        cut = conn.get_cut(ra, dec, size, band)
        cut.writeto(os.path.join(processing_folder, f'{ra}_{dec}_{size}_{band}.fits.fz'), overwrite=True)
        print(f"downloaded {ra} {dec} {size} {band}")
    
    print("")