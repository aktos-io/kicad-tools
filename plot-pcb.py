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

try:
	filename=sys.argv[1]
except:
	import glob
	filename = glob.glob('./*.kicad_pcb')[0]
	print("using kicad_pcb file: %s" % filename)


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
popt.SetOutputDirectory("plot-pcb")

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
popt.SetOutputDirectory("plot-drill")
# workaround for setting GetPlotDirName
pctl.OpenPlotfile("myworkaround", PLOT_FORMAT_SVG, "workaround")

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
popt.SetOutputDirectory("plot-assembly")

# We want *everything*
popt.SetPlotReference(True)
popt.SetPlotValue(True)
popt.SetPlotInvisibleText(True)

popt.SetDrillMarksType(PCB_PLOT_PARAMS.SMALL_DRILL_SHAPE)
pctl.SetColorMode(True)

assembly_map_files = [
    {'layer': F_Cu,     'side': "Front", 'color': 'grayed', 'mirror': False},
    {'layer': F_Paste,  'side': "Front", 'color': 'black', 'mirror': False},
    {'layer': F_Fab,    'side': "Front", 'color': 'black', 'mirror': False},

    {'layer': B_Cu,     'side': "Back", 'color': 'grayed', 'mirror': True},
    {'layer': B_Paste,  'side': "Back", 'color': 'black', 'mirror': True},
    {'layer': B_Fab,    'side': "Back", 'color': 'black', 'mirror': True},
]

popt.SetScale(1)
i = 0
for a in assembly_map_files:
    popt.SetMirror(a['mirror'])
    pctl.SetLayer(a['layer'])
    a['postfix'] = "%s_%s_%i" % (a['side'], a['color'], i)
    pctl.OpenPlotfile(a["postfix"], PLOT_FORMAT_SVG, "Assembly Layer")
    pctl.PlotLayer()
    i += 1

sides = ['Front', 'Back'] # FIXME: get from assembly_map_files list

for side in sides:
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
                    .grayed {
                        filter: opacity(20%);
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
    """.format(
        file_basename,
        side,
        '\n'.join(
            ["<img src='{0}-{1}.svg' class='stack {2}' />".format(
                file_basename, f['postfix'], f['color']
            ) for f in assembly_map_files if f['side'] == side]
        )
    )

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
try:
    with open(crop_filename, 'r') as x:
        print("WARNING: crop.css exists, not overwriting. ")
except:
    with open(crop_filename, "w") as f:
        f.write(crop_css)


pctl.ClosePlot()
