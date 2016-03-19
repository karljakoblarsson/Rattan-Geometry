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

def curve_settings(c):
    c.dimensions = '3D'
    c.fill_mode = 'FULL'
    c.bevel_resolution = 5
    c.use_uv_as_generated = True
    c.bevel_depth = bevel_depth



curvesObj = []

# """"""Trä""""" Material definerat i .blend-filen. (Ett '"' var inte nog)
material = D.materials.get('YR-Material')
texture = D.textures.get('Bamboo-tex')

# Konstanta parametrar
rows = 60
weight = 0.2

d_x = 0.5
d_y = 0.15
bend_factor = d_y
d_z = 0.08

bevel_depth = 0.03
vert_bevel_factor = 1.25


cycles = True


##############################################################################

curve = D.curves.new(name='strand', type='CURVE')

curve_settings(curve)

curvesObj.append(D.objects.new('CurveObj', curve))
C.scene.objects.link(curvesObj[0])

curvesObj[0].data.materials.append(material)

nurbs = curve.splines.new('NURBS')

count = -1
x = 0
y = bend_factor
z = 0 # z_0

# Re-meshing - Frame fields

# Glöm inte default vertexen i origo!

for strand in range(rows):

    N = 20

    if strand == 0:
        nurbs.points.add(N - 1)
    else:
        nurbs.points.add(N)

    #y = bend_factor * odd(strand)

    for n in range(N):
        count += 1
        #y = bend_factor * (odd(strand) * odd(n))
        y *= -1

        if not (n == 0):
            if odd(strand) == 1:
                x -= d_x
            else:
                x += d_x

        nurbs.points[count].co = (x, y, z, weight)

    # Slutsnurren
    nurbs.points.add(6)

    x -= odd(strand) * d_x * 0.5
    nurbs.points[count + 1].co = (x, y, z, weight)

    y *= -1
    nurbs.points[count + 2].co = (x, y, z, weight)

    x += odd(strand) * d_x * 0.5
    z += (bevel_depth)
    nurbs.points[count + 3].co = (x, y, z, weight)

    y *= -1
    z += (bevel_depth)
    nurbs.points[count + 4].co = (x, y, z, weight)

    x -= odd(strand) * d_x * 0.5
    nurbs.points[count + 5].co = (x, y, z, weight)

    y *= -1
    nurbs.points[count + 6].co = (x, y, z, weight)

    count += 6

    x += odd(strand) * d_x * 0.5
    y *= -1

    #z += bevel_depth * 4



#vert_texture = D.textures['Bamboo-tex'].copy()
#vert_texture.use_flip_axis = False
#material.texture_slots[0] = vert_texture
# nåt dumt jag gjort i .blend filenNone
vertical_strands = [None, None]

for n in range(2, N-1):
    vert = D.curves.new(name='vert_strand' + str(n), type='CURVE')

    vert.dimensions = '3D'
    vert.fill_mode = 'FULL'
    vert.bevel_resolution = 5
    vert.bevel_depth = bevel_depth * vert_bevel_factor * (1.15 - random()*0.3)
    vert.use_uv_as_generated = True


    vertical_strands.append(D.objects.new('vert_strandObj' + str(n), vert))
    C.scene.objects.link(vertical_strands[n])

    individ_mat = material.copy()
    if cycles:
        individ_mat.node_tree.nodes["Mapping"].rotation.z = random() * 180
        individ_mat.node_tree.nodes["Mapping.001"].rotation.z = random() * 180
        individ_mat.node_tree.nodes["Mapping.002"].rotation.z = random() * 180
        individ_mat.node_tree.nodes["RGB"].color.r += (random() - 0.5) * 0.1
        individ_mat.node_tree.nodes["RGB"].color.g += (random() - 0.5) * 0.1
        individ_mat.node_tree.nodes["RGB"].color.b += (random() - 0.5) * 0.1
    else:
        individ_mat.texture_slots[0].offset.y = random() * 40

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
        z += bevel_depth * 2
        nurbs.points[r].co = (x, y, z, weight)



# Render the scene and save the result if specified by the makefile using
# these enviroment variables. You're able to chang the output name using make
render = os.environ['RENDER']
if render == '1':
    outfile = os.environ.get('OUTFILE')
    if outfile is not None:
        filename = outfile
    else:
        filename = 'out/' + 'rattan.png' # Folder + default name. Should never
                                         # be called whe using the makefile.

    print(filename)
    bpy.data.scenes['Scene'].render.filepath = os.getcwd() + '/' + filename
    bpy.ops.render.render(write_still=True)

