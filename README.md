# Install 

Download this repository in any location. Add the download folder in `$PATH`: 

```bash
echo 'export PATH=$PATH:/path/to/download/folder' >> ~/.bashrc  

# if you want to use "plot-pcb remote your.svg" option, add "pcb" remote
cat >> ~/.ssh/config <<PCB_PRINTER
Host pcb
  Hostname ip.of.remote.machine
  User     youruser
PCB_PRINTER
```

# `plot-pcb.py`

Use this script to generate appropriate plot files for manufacturing PCB's with toner transfer technique. 

```bash
cd your-kicad-project
plot-pcb.py [your-kicad-project.kicad_pcb]
```
> If you omit `your-kicad-project.kicad_pcb` parameter, `plot-pcb.py` will use first `.kicad_pcb` file. 

This command generates following folders: 

* **plot-production**    : Use these plots for toner transform process. Preferably combine these layouts into one file to save toner transfer paper. Print this file from laser printer. 
* **plot-drill**         : The drill map. Print from inkjet. 
* **plot-assembly**      : Use `assembly_map_Front.html` and `assembly_map_Back.html` for getting assembly maps. Edit those html files to change the css value of `left: 1234px` to meet your needs. (TO_BE_IMPROVED)



# `print-svg`

print Kicad generated svg files via laser printer. 

## Usage 

1. Test your layout if footprints match with real ones. Flip `your.svg` horizontally and print: 

```
print-svg test your.svg
```

2. (a) Print `your.svg` directly from default printer via lpr: 

```
print-svg your.svg
```

2. (b) Print `your.svg` over ssh: 

```
print-svg remote your.svg 
```
