#!/usr/bin/python
'''
    A python script example to create various plot files from a board:
    Fab files
    Doc files
    Gerber files

    Important note:
        this python script does not plot frame references.
        the reason is it is not yet possible from a python script because plotting
        plot frame references needs loading the corresponding page layout file
        (.wks file) or the default template.

        This info (the page layout template) is not stored in the board, and therefore
        not available.

        Do not try to change SetPlotFrameRef(False) to SetPlotFrameRef(true)
        the result is the pcbnew lib will crash if you try to plot
        the unknown frame references template.
'''

import sys, os
from pcbnew import *

# output folders 
drill_folder = "plot-drill"
pcb_folder = "plot-pcb"
map_folder = "plot-assembly"

try:
	filename=sys.argv[1]
except:
	import glob
	filename = glob.glob('./*.kicad_pcb')[0]

print("using kicad_pcb file: %s" % filename)
print "------------------------------------------"


file_basename = os.path.splitext(filename)[0]

board = LoadBoard(filename)

pctl = PLOT_CONTROLLER(board)

popt = pctl.GetPlotOptions()

# Set some important plot options:
popt.SetPlotFrameRef(False)
popt.SetLineWidth(FromMM(0.35))

popt.SetAutoScale(False)
popt.SetScale(1)
popt.SetMirror(False)
popt.SetUseGerberAttributes(True)
popt.SetExcludeEdgeLayer(False);
popt.SetUseAuxOrigin(True)


# These files are needed in production
# ########################################
print "+ Generating copper layer ({0})".format(pcb_folder)
popt.SetOutputDirectory(pcb_folder)

# make sure that everything in plot-pcb folder is being renewed
if len(os.listdir(pcb_folder)) > 2:
    print "----------------------------------------------------"
    print "!! Delete additional files in {0} folder to make sure every file is up to date".format(pcb_folder)
    exit()


# Top Layer
popt.SetDrillMarksType(PCB_PLOT_PARAMS.SMALL_DRILL_SHAPE)
popt.SetMirror(True)
pctl.SetLayer(F_Cu)
pctl.OpenPlotfile("layer-F_Cu", PLOT_FORMAT_SVG, "Top Layer")
pctl.PlotLayer()

# Bottom Layer
popt.SetDrillMarksType(PCB_PLOT_PARAMS.SMALL_DRILL_SHAPE)
popt.SetMirror(False)
pctl.SetLayer(B_Cu)
pctl.OpenPlotfile("layer-B_Cu", PLOT_FORMAT_SVG, "Bottom Layer")
pctl.PlotLayer()


# Drill map
print "+ Generating drill file ({0})".format(drill_folder)
popt.SetOutputDirectory(drill_folder)

# FIXME: workaround for setting GetPlotDirName
workaround_name = "workaround"
pctl.OpenPlotfile(workaround_name, PLOT_FORMAT_SVG, workaround_name)
workaround_file = os.path.join(pctl.GetPlotDirName(), (file_basename + '-' +  workaround_name + ".svg"))
os.remove(workaround_file)

drlwriter = EXCELLON_WRITER( board )
drlwriter.SetMapFileFormat( PLOT_FORMAT_PDF )

mirror = False
minimalHeader = False
offset = wxPoint(0,0)
# False to generate 2 separate drill files (one for plated holes, one for non plated holes)
# True to generate only one drill file
mergeNPTH = True
drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH )

metricFmt = True
drlwriter.SetFormat( metricFmt )

genDrl = True
genMap = True
drlwriter.CreateDrillandMapFilesSet( pctl.GetPlotDirName(), genDrl, genMap );



# Assembly Map
# ######################################################
mirrored = {
    'F': False,
    'B': True
}

layers = [
    'Cu',
    'SilkS',
    #'Fab',
    'Paste'
    ]

print "+ Generating assembly map ({0}) with layers: {1}".format(
    map_folder,
    ', '.join(layers) )
popt.SetOutputDirectory(map_folder)

# We want *everything*
popt.SetPlotReference(True)
popt.SetPlotValue(True)
popt.SetPlotInvisibleText(True)

popt.SetDrillMarksType(PCB_PLOT_PARAMS.SMALL_DRILL_SHAPE)
pctl.SetColorMode(True)
popt.SetScale(1)

def get_layer(side, layer):
    return eval(side.upper() + '_' + layer)


for side in mirrored:
    images = ''
    for layer in layers:
        name = side + '_' + layer
        images += "<img src='{0}-{1}.svg' class='stack {2}' />\n".format(file_basename, name, layer)

        popt.SetMirror(mirrored[side])
        pctl.SetLayer(get_layer(side, layer))
        pctl.OpenPlotfile(name, PLOT_FORMAT_SVG, "Assembly Layer")
        pctl.PlotLayer()

    # generate html files
    assembly_html = """
        <html>
            <head>
                <style>
                    @page {
                        size: landscape;
                        margin: 0;
                    }
                    img {
                        max-width: 100%;
                        max-height; 100%;
                    }
                    body {
                        padding: 5mm;
                    }
                    .stack {
                        position: absolute;
                    }
                    .container {
                        height: 190mm;
                        position: relative;
                        overflow: hidden;
                        border: 1px dashed black;

                    }
                    /* ---------- LAYERS ---------- */
                    .Cu {
                        filter: opacity(18%);
                    }
                    .SilkS {
                        filter: opacity(50%);
                    }
                    .Paste {
                        filter: opacity(90%);
                    }
                </style>
                <link rel="stylesheet" type="text/css" href="./crop.css">
            </head>
    """
    assembly_html += """
            <body>
                <div class="container">
                    <h3><center>{0} ({1})</center></h3>
                    {2}
                </div>
            </body>
        </html>
    """.format(file_basename, side, images)

    html_filename = os.path.join(pctl.GetPlotDirName(), 'assembly_map_{}.html'.format(side))
    with open(html_filename, "w") as f:
        f.write(assembly_html)


# fine tune with crop.css
crop_css = """
    img {
        transform: scale(2.3);
        position: relative;
        top: 180px;
        /* do not use `left: ...` or `right: ...` */
    }
    """
crop_filename = os.path.join(pctl.GetPlotDirName(), 'crop.css')
print "------------------------------------------"
try:
    with open(crop_filename, 'r') as x:
        print "crop.css already exists, not overwriting. "
except:
    with open(crop_filename, "w") as f:
        f.write(crop_css)
        print ''
        print '    TIP: Use crop.css for fine tuning (this file will not be overwritten)'
        print ''


pctl.ClosePlot()
