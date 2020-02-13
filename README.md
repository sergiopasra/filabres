# filabres

Automatic Data Reduction Pipeline for CAHA data.

To install the code, clone the repository and execute:
```
$ cd filabres
$ python setup.py build
$ python setup.py install
```

It is recommendable to run the code from an empty directory.

### Initialize the auxiliary image databases
```
$ filabres -i cafos -dd ~/CAFOS2017 -n 17????_t2_CAFOS -rs initialize
```
The previous command generates a subdirectory `lists` in the current
directory, with a tree of observing nights. Within each night a file called
`imagedb_cafos.json` stores the image classification (i.e., bias, flat-imaging,
science-imaging,...) following the requirements described in the file 
`filabes/instrument/configuration.yaml`.

### Compute combined bias images
```
$ filabres -i cafos -dd ~/CAFOS2017 -n 17????_t2_CAFOS -rs bias
```

### Compute combined flat-imaging images
```
$ filabres -i cafos -dd ~/CAFOS2017 -n 17????_t2_CAFOS -rs flat-imaging
```
