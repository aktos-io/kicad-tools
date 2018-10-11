# Install

Clone or download this repository in any location. Add the download folder in `$PATH` in `.bashrc`.

## Dependencies

* inkscape

# `kicad-gen-fabrication`

Use this script to generate appropriate plot files for manufacturing PCB's with toner transfer technique and generate needed files for mass production.

```bash
cd your-kicad-project
kicad-gen-fabrication [your-kicad-project.kicad_pcb]
```
> Default pcb file is the first `.kicad_pcb` file found.

This command generates following folders:

- **prototype** : Files used for prototyping
    * **copper**    : Use these outputs for toner transform process. TIP: Combine these layouts into one A4 to save toner transfer paper. Print this file from laser printer.
    * **drill**     : The drill map. Print from inkjet.
    * **assembly**  : Use `assembly_map_Front.html` and `assembly_map_Back.html` for getting assembly maps. Edit those html files to change the css value of `left: 1234px` to meet your needs. (TO_BE_IMPROVED)
- **fabrication** : Files used for mass production (gerber files)

# `print-svg`

Prints svg files accurately. See `print-svg --help`

# `kicad-use-component`

Use a pre-defined schematic file from a library. See `kicad-use-component --help`
