#python
#Take list file with parents and make a tex diagram of the product tree.
# Top of the tree will be left of the page .. this allow a LONG list of products. 

import os
import fileinput
from treelib import Node, Tree

#pt sizes for box + margin + gap between boex
txtheight=22
sep=2  # inner sep
gap=4
WBS=1

class Product(object): 
    def __init__(self, id, name, parent, desc, wbs, manager, owner): 
        self.id = id
        self.name = name
        self.parent = parent
        self.desc = desc
        self.wbs = wbs
        self.manager=manager
        self.owner=owner

def constructTree(fin ):
    "Read the tree file and ocntrcut a tree structure"
    count=0
    ptree = Tree()
    for line in fin :
        if line.startswith(",,,,") or line.startswith("id,Item,"):
                continue
        count= count + 1
        line=line.replace("\"","")
        part=line.split(","); #id,prod, parent, descr ..
        
        prod= Product(part[0],part[1],part[2],part[3],part[4],part[5],part[6])
        #print "Product:"+ prod.id + " name:"+prod.name+" parent:"+prod.parent
        if (count==1) : # root node
            ptree.create_node(prod.id, prod.id, data=prod)
        else:
            #print "Creating node:"+ prod.id + " name:"+prod.name+" parent:"+prod.parent
            if prod.parent != "":
                ptree.create_node(prod.id,prod.id,data=prod, parent=prod.parent)
            else:
                fout.write(part[0]+ " no parent \n")

    print  str(count) + " Product lines \n"
    return ptree;

def outputTexTree(tout,fout, ptree ):
    fnodes=[];
    nodes=ptree.expand_tree()
    count=0
    prev=Product("n","n","n","n","n","n","n")
    blocksize=txtheight +gap + sep   # Text height  + the gap added to each one
    for n in  nodes:
        prod = ptree[n].data
        fnodes.append(prod)
        depth=ptree.depth(n)
        count=count+1
        tout.write("{\\tiny "+prod.wbs+"} & \\small "+prod.name+" & "+ prod.desc+" & " + prod.manager+" & "+prod.owner+ "\\\\ \hline \n")
        #print str(depth)+" Product:"+ prod.id + " name:"+prod.name+" parent:"+prod.parent
        if (count==1) : # root node
            fout.write("\\node ("+prod.id+") [wbbox]{\\textbf{"+prod.name+"}}; \n");
        else:
            fout.write("\\node ("+prod.id+") [pbox,")
            if (prev.parent <> prod.parent) : # first child to the right
                found=0
                scount=count-1
                while found==0 and scount>0:
                    scount=scount-1
                    found =  fnodes[scount].parent==prod.parent
                if  scount<=0 :  # first sib can go righ of parent
                    fout.write("right=15mm of "+prod.parent) 
                else: #Figure how low to go  - find my prior sibling
                    psib=fnodes[scount];
                    leaves=ptree.leaves(psib.id)
                    depth=len(leaves)
                    lleaf=leaves[depth-1].data
                    #print "Prev:"+prev.id + " psib:"+psib.id + " lleaf.parent:"+lleaf.parent
                    if (lleaf.parent==psib.id): depth = depth -1 
                    #if (prod.id=="L2") : depth=depth+1 # Not sure why this is one short .. 
                    dist=depth* blocksize # the numbe rof leaves below my sibling
                    #print prod.id+" Depth:"+str(depth)+" dist:"+str(dist) + " blocksize:"+str(blocksize)+ " siblin:"+psib.id
                    fout.write("below="+str(dist)+"pt of "+psib.id) 
            else : # benetih the sibling
                dist=gap
                fout.write("below="+str(dist)+"pt of "+prev.id) 
            fout.write("] {")
            if WBS ==1 and prod.wbs != "":
                fout.write("{\\tiny \\color{gray}"+prod.wbs+"} ")
                fout.write("\\newline")
            fout.write("\\textbf{"+prod.name+"}")
            fout.write("}; \n")
            fout.write(" \draw[pline] ("+prod.parent+".east) -| ++(0.4,0)  |- ("+prod.id+".west);\n ")
        prev=prod;
    print  str(count) + " Product lines in TeX \n"
    return

def doFile(inFile ):
	"This processes a csv and produced a  tex tree diagram and a tex longtable."
	f=inFile 
	nf = "ProductTree.tex"
	nt = "productlist.tex"
	print "Processing " + f  +"-> (figure)"+ nf + " and (table)" + nt
	fin = open (f,'r')  	
        ptree=constructTree(fin)

        #ptree.show(data_property="name")
	fout = open (nf,'w')  	
	tout = open (nt,'w')  	

        width = ptree.depth() * 6 # cm
        heigth = len(ptree.leaves()) * 1 # cm
        header(fout,width,heigth)
        theader(tout)

        outputTexTree(tout, fout, ptree)

        footer(fout)
        tfooter(tout)
	fout.close()
	fin.close()

	return;
 # End DoDir


def theader(tout):
     tout.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
     tout.write("%%  Product table generated by "+__file__+" do not modify.")
     tout.write("\n")
     tout.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
     tout.write("\n")
     tout.write("\\begin{longtable}{|p{0.1\\textwidth}|p{0.2\\textwidth}|p{0.4\\textwidth}|p{0.15\\textwidth}|p{0.15\\textwidth}|}\hline \n ")
     tout.write("\\bf WBS & Product & Description & Manager & Owner \\\\ \hline   \n")

     return

def header(fout,pwidth,pheigth):
     fout.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
     fout.write("\n")
     fout.write("%")
     fout.write("\n")
     fout.write("% Document:      DM  product tree")
     fout.write("\n")
     fout.write("%")
     fout.write("\n")
     fout.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
     fout.write("\n")

     fout.write("\documentclass{article}")
     fout.write("\n")

     fout.write("\usepackage{times,layouts}")
     fout.write("\n")
     fout.write("\usepackage{tikz,hyperref,amsmath}")
     fout.write("\n")
     fout.write("\usetikzlibrary{positioning,arrows,shapes,decorations.shapes,shapes.arrows}")
     fout.write("\n")
     fout.write("\usetikzlibrary{backgrounds,calc}")
     fout.write("\n")

     fout.write("\usepackage[paperwidth="+str(pwidth)+"cm,paperheight="+str(pheigth)+"cm,")
     fout.write("\n")
     fout.write("left=-2mm,top=3mm,bottom=0mm,right=0mm,")
     fout.write("\n")
     fout.write("noheadfoot,marginparwidth=0pt,includemp=false,")
     fout.write("\n")
     fout.write("textwidth=30cm,textheight=50mm]{geometry}")
     fout.write("\n")


     fout.write("\\newcommand\showpage{%")
     fout.write("\n")
     fout.write("\setlayoutscale{0.5}\setlabelfont{\\tiny}\printheadingsfalse\printparametersfalse")
     fout.write("\n")
     fout.write("\currentpage\pagedesign}")
     fout.write("\n")

     fout.write("\hypersetup{pdftitle={DM organisation }, pdfsubject={Diagram illustrating the")
     fout.write("\n")
     fout.write("products in LSST DM }, pdfauthor={ William O\'Mullane}}")
     fout.write("\n")

     fout.write("\\tikzstyle{wbbox}=[rectangle, rounded corners=3pt, draw=black, top color=blue!50!white, bottom color=white, very thick, minimum height=12mm, inner sep=2pt, text centered, text width=30mm] \n")
     fout.write("\\tikzstyle{pbox}=[rectangle, rounded corners=3pt, draw=black, top color=yellow!50!white, bottom color=white, very thick, minimum height="+str(txtheight)+"pt, inner sep="+str(sep)+"pt, text centered, text width=35mm] \n")
     fout.write("\\tikzstyle{pline}=[-, thick]")


     fout.write("\\begin{document}\n")
     fout.write("\\begin{tikzpicture}[node distance=0mm]\n")
     return;

def footer(fout):
     fout.write("\end{tikzpicture}\n")
     fout.write("\end{document}\n")
     return;

def tfooter(tout):
     tout.write("\end{longtable} \n")
     return;


### MAIN 
doFile("productlist.csv")
