## single object photometry

![](https://splus.cloud/images/splus_logo_fundo_branco.jpg)

### Get photometry of a single object using splusdata

Instructions: 

#### 1st step: 
If you dont have astromatic/sextractor installed, you may run with docker:

```
docker-compose up --build
``` 

This will run the container. 

----
If you have sextractor installed just leave sextr/runner.py running aside. It's important to run from the folder because of the relative paths:

```
cd sextr && runner.py
```

<br>

*Leave this step running on one tab, then open another terminal tab/window to step 2.*

<br>

### 2nd step: 

Just run main.py to get the splusdata, login with your splus.cloud account and follow the instructions:

```
python3 main.py
```

<br>

### 3rd step (Not needed if inputing tables on step 2)

Run join_tables.py, pass the ra, dec and size of object to locate result folder, get center object, join tables and produce final table result. 
The input here should be *RA_DEC_size*, something like:

- 0.1_0.1_250 (the same name as the result folder inside sextr/shared/processed_folder)

Run script by:
```
python3 join_tables.py
```

<br>
<br>

### Results

All results may be found at:
sextr/shared/processed_folder


#### Minors:

If the program isn't producing the final table, you may manually run replacing the values:

```
python3 join_tables.py {RA}_{DEC}_{SIZE}
```


<br>
<br>
Written by Gustavo Schwarz 

