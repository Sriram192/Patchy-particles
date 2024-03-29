#!/usr/bin/tclsh

# topotools example 1b:
# generate topology data from coordinate data
# for a simple linear chain of model particles.
##############################################

# explicitly load topotools and pbctools packages since
# they are not automatically requred in text mode and
# abort if their version numbers are insufficient.
if {[catch {package require topotools 1.1} ver]} {
   vmdcon -error "$ver. This script requires at least TopoTools v1.1. Exiting..."
   quit
}
if {[catch {package require pbctools 2.3} ver]} {
   vmdcon -error "$ver. This script requires at least pbctools v2.3. Exiting..."
   quit
}
# load coordinates but don't automatically compute bonds
mol new packed.xyz autobonds no waitfor all

# set atom name/type and radius for all atoms
set sel [atomselect top {name A}]
$sel set radius 0.05
$sel set name A
$sel set type A
$sel set mass 1.0

set sel2 [atomselect top {name B}]
$sel2 set radius 0.85
$sel2 set name B
$sel2 set type B
$sel2 set mass 1.0

# bonds are computed based on distance criterion
# bond if 0.6 * (r_A + r_B) > r_AB.
# with radius 0.85 the cutoff is 1.02
# the example system has particles 1.0 apart.
mol bondsrecalc top

# now recompute bond types. 
# by default a string label: <atom type 1>-<atom type 2>
# we have two atom types A and B, but type B atoms are only
# at the end of the chain, so there should be only two bond
# types: A-A and A-B. Bond type B-A is identical to A-B and
# will be made canonical (lower string value first) by topotools.
topo retypebonds 
vmdcon -info "assigned [topo numbondtypes] bond types to [topo numbonds] bonds:"
vmdcon -info "bondtypes: [topo bondtypenames]"



# now derive angle definitions from bond topology.
# every two bonds that share an atom yield an angle.
topo guessangles
vmdcon -info "assigned [topo numangletypes] angle types to [topo numangles] angles:"
vmdcon -info "angletypes: [topo angletypenames]"

# now let VMD reanalyze the molecular structure
# this is needed to detect fragments/molecules
# after we have recomputed the bonds
mol reanalyze top
mol list



# now set box dimensions and write out the result as 
# a lammps data ifile.
pbc set {46.42 46.42 46.42 90.0 90.0 90.0}
topo writelammpsdata data.packed angle
animate write psf data.psf

#set sel3 [atomselect top all]
#$sel3 writexyz vmd_packed.xyz
#$sel3 delete
