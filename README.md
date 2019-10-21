# Plotter-3000

Plotter-3000 is a python library that implements numpy, scipy and matplotlib to generate an 
automated data processor and plotter designed specially for use in pure and applied sciences.

## Usage

```python
from Graphing import Plotter

p = Plotter('path/to/your/file.txt') # opens and processes a .txt file with data

p.scatter() # plots and saves a scatter plot of the file
p.lines() # plots and saves with lines the file
p.histogram() # plots and saves a histogram 
p.frequency() # plots and saves a relative frequency polygon
```

## Roadmap
* Support for all file extension
* Automated error management

## Acknowledgments 
* Hats off to the developers of numpy, scipy and matplotlib, libraries on which this proyect 
is based