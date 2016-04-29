# Hej! Den här koden är int lika skit aom tidigare. Men kanske inte bra.
# Klaga inte på att den är sämst, jag vet det redan. :P

import bpy
import os, sys
from mathutils import *
from math import *
from random import *

#### TODO
# - Take panel settings - Sort of done
# - Fix bevel_depth based on height, or the other way around
# - Kontakta ICOM
# - Weaving

# Convenience Variables:
C = bpy.context
D = bpy.data

def odd(n):
    return (2*(n%2)) - 1

##############################################################################

def create_rattan(transform, rows=60, N=20, bevel_depth = 0.03):
    # Konstanta parametrar
    weight = 0.2

    d_x = 1/N
    d_y = 6.0 * bevel_depth
    d_z = 1/rows


    vert_bevel_factor = 1.05

    rattan_obj = D.objects.new('Rattan', None)
    C.scene.objects.link(rattan_obj)


    def curve_settings(c, depth = bevel_depth):
        c.dimensions = '3D'
        c.fill_mode = 'FULL'
        c.bevel_resolution = 5
        c.use_uv_as_generated = True
        c.bevel_depth = depth


    curve = D.curves.new(name='Wrap', type='CURVE')

    curve_settings(curve)

    curves_obj = D.objects.new('Wrap', curve)
    curves_obj.parent = rattan_obj
    C.scene.objects.link(curves_obj)

    nurbs = curve.splines.new('NURBS')

    count = -1
    x = 0
    y = d_y
    z = 0

    def set_point(count, vector):
        point = Vector((0,0,0,weight))
        point.xyz = transform(Vector(vector))
        nurbs.points[count].co = point

    for strand in range(rows):

        if strand == 0:
            nurbs.points.add(N - 1)
        else:
            nurbs.points.add(N)

        for n in range(N):
            count += 1
            y *= -1

            if not (n == 0):
                if odd(strand) == 1:
                    x -= d_x
                else:
                    x += d_x

            set_point(count, (x, y, z))

        # Slutsnurren
        # Det här borde vi kanske gör annorlunda
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


    weight = 0.2

    def set_vert_point(spline, count, vector):
        point = Vector((0, 0, 0, weight))
        point.xyz = transform(Vector(vector))
        spline.points[count].co = point

    verticals = D.curves.new(name='Weft', type='CURVE')

    curve_settings(verticals, bevel_depth * vert_bevel_factor)

    vertical_strands = (D.objects.new('Weft', verticals))

    vertical_strands.parent = rattan_obj
    C.scene.objects.link(vertical_strands)

    x = 0
    y = 0

    for n in range(0, N-2):
        nurbs = verticals.splines.new('NURBS')

        nurbs.use_endpoint_u = True

        nurbs.points.add(rows-1)

        x += d_x
        z = 0

        for r in range(rows):
            z += d_z * 2
            set_vert_point(nurbs, r, (x, y, z))


    curves_obj.select = True
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')



class RattanOperator(bpy.types.Operator):
    bl_idname = "object.rattan"
    bl_label = "Create Rattan Operator"

    def execute(self, context):
        print("Create Rattan")

        obj = C.selected_objects[0]
        location = obj.location

        # Transform so the center is in the origin
        mat_init_trans = Matrix.Translation(Vector((-0.5,0,-1.0)))
        # Translate according to input
        mat_trans = Matrix.Translation(location)

        (xs, ys, zs) = obj.scale

        mat_scale_u = Matrix.Scale(xs*2, 4, (1.0, 0.0, 0.0))
        mat_scale_v = Matrix.Scale(zs, 4, (0.0, 0.0, 1.0))
        mat_scale_w = Matrix.Scale(1.0, 4, (0.0, 1.0, 0.0))

        mat_scale = mat_scale_u * mat_scale_v * mat_scale_w

        def trans(vector):
            return mat_trans * mat_scale * mat_init_trans * vector

        obj.select = False
        create_rattan(trans, C.scene.rattan_rows, C.scene.rattan_cols,
                C.scene.rattan_bevel_depth)
        return {'FINISHED'}

bpy.utils.register_class(RattanOperator)


class RattanPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_hello_world"
    bl_label = "Rattan generator"
    bl_category = "Tools"
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    bpy.types.Scene.rattan_rows = bpy.props.IntProperty(name = "Rows",
            default = 40)
    bpy.types.Scene.rattan_cols = bpy.props.IntProperty(name = "Cols",
            default = 20)
    bpy.types.Scene.rattan_bevel_depth = bpy.props.FloatProperty(
            name = "Bevel depth", default = 0.03)


    def draw(self, context):
        print(dir(context))
        self.layout.prop(context.scene, "rattan_rows")
        self.layout.prop(context.scene, "rattan_cols")
        self.layout.prop(context.scene, "rattan_bevel_depth")
        self.layout.operator("object.rattan", text="Create Rattan", icon="PLUS")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

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


