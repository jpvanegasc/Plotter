# Plotter-3000

Plotter-3000 is a Python library that implements numpy, scipy and matplotlib to support an 
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
## Example

```python
from Graphing import Plotter
import os

def mod_y(value):
    return value + 10

path =  '/path/to/folder/'
docs = sorted(os.listdir(path))

filtered_docs = [x for x in docs if x.split('.')[-1] == 'txt']
total = len(filtered_docs)

for i, d in enumerate(filtered_docs):
    p = Plotter(path+d, f_y=mod_y) # Load each file and modify y-values using mod_y
    p.multiple_graphs = True # Plots multiple files on a single graph
    p.color = i # Changes color for each dataset using a default colorlist
    p.no_title = True 

    if i == total-1: # Plots all the folder files on a single graph
        p.multiple_graphs = False 

    p.y = (r'S', r'dim_less') # Changes y labels to "S". Note, dim_less keyword omits dimensions
    p.x = (r't', r's') # Changes x labels to "t(s)"
    
    p.lines(label = p.clean_name) # Plots each dataset 
```

## Roadmap
* Support for all file extensions
* Automated experimental error processing and management

## Acknowledgments 
* Hats off to the developers of numpy, scipy and matplotlib, libraries which made this 
proyect posible