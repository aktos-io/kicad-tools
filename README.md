# Install 

Download this repository in any location. Add the download folder in `$PATH`: 

```
echo 'export PATH=$PATH:/path/to/download/folder' >> ~/.bashrc  
```

# `plot-pcb.py`

Use this script to generate appropriate plot files for manufacturing PCB's with toner transfer technique. 

```
cd your-kicad-project
plot-pcb.py [your-kicad-project.kicad_pcb]
```
> If you omit `your-kicad-project.kicad_pcb` parameter, `plot-pcb.py` will use first `.kicad_pcb` file. 

This command generates following folders: 

* plot-test: Use this svg files for testing if every footprint matches with real measurements or not. Print from inkjet. 
* plot-production: Use these plots for toner transform process. Print from laser printer. 
* plot-drill: The drill map. Print from inkjet. 
* plot-assembly: Use `*-Front.html` and `*-Back.html` for getting assembly maps. Edit those html files to change `left: 1234px` value to fit your schema. 



# `print-svg`

print Kicad generated svg files via laser printer. 

## Usage 

Flip `your.svg` horizontally to create test output: 

```
print-svg test your.svg
```

Print `your.svg` directly from default printer via lpr: 

```
print-svg your.svg
```

Print `your.svg` over ssh: 

```
print-svg remote your.svg 
```
