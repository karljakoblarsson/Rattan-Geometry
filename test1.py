# Hej! Den här koden är skit. Den är bara ihopslängd för att testa hur blender
# funkar. Klaga inte på att den är sämst, jag vet det redan. :P

import bpy
import os, sys
from mathutils import *
from math import *
from random import *

# Convenience Variables:
C = bpy.context
D = bpy.data

def odd(n):
    return (2*(n%2)) - 1

curvesObj = []

# """"""Trä""""" Material definerat i .blend-filen. (Ett '"' var inte nog)
material = D.materials.get('YR-Material')
texture = D.textures.get('Bamboo-tex')

# Konstanta parametrar
rows = 40
weight = 0.2

d_x = 0.5
d_y = 0.3
bend_factor = d_y
d_z = 0.08

bevel_depth = 0.04
vert_bevel_factor = 1.25

z = 0 # z_0

for strand in range(rows):

    curve = D.curves.new(name='strand' + str(strand), type='CURVE')

    curve.dimensions = '3D'
    curve.fill_mode = 'FULL'
    curve.bevel_resolution = 5
    curve.bevel_depth = bevel_depth * (1.25 - random()*0.5)


    curvesObj.append(D.objects.new('CurveObj' + str(strand), curve))
    C.scene.objects.link(curvesObj[strand])

    #individ_mat = material.copy()
    curvesObj[strand].data.materials.append(material)


    nurbs = curve.splines.new('NURBS')

    # Funkar inte här. Ser ut somm stryk
    #curve.splines[0].use_endpoint_u = True

    N = 20

    nurbs.points.add(N-1)

    x, y = 0, 0
    z += d_z + (random() * 0.030 - 0.0150)

    for n in range(N):
        #x = n/2
        y = bend_factor * (odd(strand) * odd(n))
        #z = strand/4
        x += d_x
        #y += d_y
        nurbs.points[n].co = (x, y, z, weight)


# nåt dumt jag gjort i .blend filenNone
vertical_strands = [None, None]

for n in range(2, N-1):
    vert = D.curves.new(name='vert_strand' + str(n), type='CURVE')

    vert.dimensions = '3D'
    vert.fill_mode = 'FULL'
    vert.bevel_resolution = 5
    vert.bevel_depth = bevel_depth * vert_bevel_factor * (1.15 - random()*0.3)


    vertical_strands.append(D.objects.new('vert_strandObj' + str(n), vert))
    C.scene.objects.link(vertical_strands[n])

    individ_mat = material.copy()
    vertical_strands[n].data.materials.append(individ_mat)

    nurbs = vert.splines.new('NURBS')

    # finns först här. Använd hela splinen
    vert.splines[0].use_endpoint_u = True

    nurbs.points.add(rows-1)

    weight = 0.2

    z = 0

    for r in range(rows):
        x = n/2
        y = 0
        #z = r/4
        z += d_z
        nurbs.points[r].co = (x, y, z, weight)



# Det här ska se till att bilden sparas i mappen out som ignoreras av git.
if len(sys.argv) == 0:
    filename = 'rattan.png'
    bpy.data.scenes['Scene'].render.filepath = os.getcwd() + '/out/' + filename
    bpy.ops.render.render(write_still=True)

