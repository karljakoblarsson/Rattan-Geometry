# Hej! Den här koden är skit. Den är bara ihopslängd för att testa hur blender
# funkar. Klaga inte på att den är sämst, jag vet det redan. :P

import bpy
import os, sys
from mathutils import *
from math import *
from random import *

#### TODO
# - Fixa ordentligt UV in [0,1]
# - Take input
# - And settings
# - Group veert_strands somehow
# - Kontakta ICOM
# - Weaving

# Convenience Variables:
C = bpy.context
D = bpy.data

def odd(n):
    return (2*(n%2)) - 1

##############################################################################

def create_rattan(transform, rows=60, N=20):
    # """"""Trä""""" Material definerat i .blend-filen. (Ett '"' var inte nog)
    material = D.materials.get('YR-Material')
    texture = D.textures.get('Bamboo-tex')

    # Konstanta parametrar
    weight = 0.2

    d_x = 1/N
    d_y = 0.15
    bend_factor = d_y
    d_z = 1/rows

    bevel_depth = 0.03

    vert_bevel_factor = 1.25


    cycles = False

    def curve_settings(c):
        c.dimensions = '3D'
        c.fill_mode = 'FULL'
        c.bevel_resolution = 5
        c.use_uv_as_generated = True
        c.bevel_depth = bevel_depth


    curve = D.curves.new(name='strand', type='CURVE')

    curve_settings(curve)

    curvesObj = D.objects.new('CurveObj', curve)
    C.scene.objects.link(curvesObj)

    curvesObj.data.materials.append(material)

    nurbs = curve.splines.new('NURBS')

    count = -1
    x = 0
    y = bend_factor
    z = 0 # z_0

    def set_point(count, vector):
        (xn, yn, zn) = transform(Vector(vector))
        nurbs.points[count].co = (xn, yn, zn, weight)


    # Glöm inte default vertexen i origo!

    for strand in range(rows):

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

            set_point(count, (x, y, z))

        # Slutsnurren
        nurbs.points.add(6)

        x -= odd(strand) * d_x * 0.5
        set_point(count + 1, (x, y, z))

        y *= -1
        set_point(count + 2, (x, y, z))

        x += odd(strand) * d_x * 0.5
        z += (d_z)
        set_point(count + 3, (x, y, z))

        y *= -1
        z += (d_z)
        set_point(count + 4, (x, y, z))

        x -= odd(strand) * d_x * 0.5
        set_point(count + 5, (x, y, z))

        y *= -1
        set_point(count + 6, (x, y, z))

        count += 6

        x += odd(strand) * d_x * 0.5
        y *= -1


    #vert_texture = D.textures['Bamboo-tex'].copy()
    #vert_texture.use_flip_axis = False
    #material.texture_slots[0] = vert_texture
    # nåt dumt jag gjort i .blend filenNone
    #vertical_strands = [None, None]

    #for n in range(2, N-1):
        #vert = D.curves.new(name='vert_strand' + str(n), type='CURVE')

        #vert.dimensions = '3D'
        #vert.fill_mode = 'FULL'
        #vert.bevel_resolution = 5
        #vert.bevel_depth = bevel_depth * vert_bevel_factor * (1.15 - random()*0.3)
        #vert.use_uv_as_generated = True


        #vertical_strands.append(D.objects.new('vert_strandObj' + str(n), vert))
        #C.scene.objects.link(vertical_strands[n])

        #individ_mat = material.copy()
        #if cycles:
            #individ_mat.node_tree.nodes["Mapping"].rotation.z = random() * 180
            #individ_mat.node_tree.nodes["Mapping.001"].rotation.z = random() * 180
            #individ_mat.node_tree.nodes["Mapping.002"].rotation.z = random() * 180
            #individ_mat.node_tree.nodes["RGB"].color.r += (random() - 0.5) * 0.1
            #individ_mat.node_tree.nodes["RGB"].color.g += (random() - 0.5) * 0.1
            #individ_mat.node_tree.nodes["RGB"].color.b += (random() - 0.5) * 0.1
        #else:
            #individ_mat.texture_slots[0].offset.y = random() * 40

        #vertical_strands[n].data.materials.append(individ_mat)

        #nurbs = vert.splines.new('NURBS')

        ## finns först här. Använd hela splinen
        #vert.splines[0].use_endpoint_u = True

        #nurbs.points.add(rows-1)

        #weight = 0.2

        #z = 0

        #for r in range(rows):
            #x = n/2
            #y = 0
            ##z = r/4
            #z += bevel_depth * 2
            #nurbs.points[r].co = (x, y, z, weight)

    curvesObj.select = True
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')



class RattanOperator(bpy.types.Operator):
    bl_idname = "object.rattan"
    bl_label = "Create Rattan Operator"

    #my_height = bpy.props.IntProperty(name="Height")

    def execute(self, context):
        print("Create Rattan")

        obj = C.selected_objects[0]
        d_vec = obj.location

        mat_init_trans = Matrix.Translation(Vector((-0.5,0,-1.0)))
        mat_trans = Matrix.Translation(d_vec)

        (xs, ys, zs) = obj.scale

        # Eeeh, it works. But probably needs to be more robust.
        mat_scale_u = Matrix.Scale(xs*2, 4, (1.0, 0.0, 0.0))
        mat_scale_v = Matrix.Scale(zs, 4, (0.0, 0.0, 1.0))
        mat_scale_w = Matrix.Scale(ys*2, 4, (0.0, 1.0, 0.0))

        mat_scale = mat_scale_u * mat_scale_v * mat_scale_w

        def trans(vector):
            (xn, yn, zn) = mat_trans * mat_scale * mat_init_trans * vector
            return (xn, yn, zn)

        #bpy.ops.object.delete()
        obj.select = False
        create_rattan(trans, 80, 30)
        return {'FINISHED'}

bpy.utils.register_class(RattanOperator)


class RattanPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_hello_world"
    bl_label = "Tjabba!"
    bl_category = "Tools"
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        #self.layout.label(text="Hello World")
        self.layout.label(text="This is rad!")
        #self.layout.prop(bpy.ops.object.rattan, "my_height")
        self.layout.operator("object.rattan", text="Create Rattan", icon="PLUS")

bpy.utils.register_class(RattanPanel)


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


