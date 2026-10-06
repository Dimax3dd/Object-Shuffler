bl_info = {
    "name": "Object Shuffler",
    "author": "OpenAI",
    "version": (1, 3, 0),
    "blender": (5, 1, 0),
    "category": "Object",
}


import bpy
import re

from random import choice, sample, uniform
from math import radians
from mathutils import Euler



# ============================================================
# HELPERS
# ============================================================


def selected():

    return list(
        bpy.context.selected_objects
    )



def deselect():

    for o in bpy.context.selected_objects:

        o.select_set(False)



def select(objects):

    for o in objects:

        if o:

            o.select_set(True)



# ------------------------------------------------------------
# OBJECT NAME CLEANER
# ------------------------------------------------------------

def base_name(name):

    """
    Removes Blender numbering and custom numbering:

    Cube.001 -> Cube
    LAMP_001 -> LAMP
    TREE-002 -> TREE
    """

    name = name.split(".")[0]


    name = re.sub(
        r'[_\-\s]?\d+$',
        '',
        name
    )


    return name



def make_copy(source, collection):


    if source.instance_type == "COLLECTION":

        obj = bpy.data.objects.new(
            source.name,
            None
        )

        obj.instance_type = "COLLECTION"

        obj.instance_collection = (
            source.instance_collection
        )


    else:

        obj = source.copy()

        if source.data:

            obj.data = source.data



    collection.objects.link(obj)


    return obj




# ============================================================
# PROPERTIES
# ============================================================


def register_properties():


    S = bpy.types.Scene



    S.os_replace_type = bpy.props.EnumProperty(

        name="Replace Type",

        items=[

            (
                "OBJECT",
                "Object",
                ""
            ),

            (
                "COLLECTION",
                "Collection",
                ""
            )

        ],

        default="OBJECT"

    )



    S.os_object = bpy.props.PointerProperty(

        type=bpy.types.Object

    )



    S.os_collection = bpy.props.PointerProperty(

        type=bpy.types.Collection

    )



    S.os_keep = bpy.props.IntProperty(

        name="Keep %",

        default=50,

        min=1,

        max=100

    )



    S.os_rot_x = bpy.props.BoolProperty(

        default=False

    )


    S.os_rot_y = bpy.props.BoolProperty(

        default=False

    )


    S.os_rot_z = bpy.props.BoolProperty(

        default=True

    )



    S.os_scale_min = bpy.props.FloatProperty(

        default=0.8

    )


    S.os_scale_max = bpy.props.FloatProperty(

        default=1.2

    )



    S.os_scale_uniform = bpy.props.BoolProperty(

        default=True

    )


    S.os_scale_x = bpy.props.BoolProperty(

        default=True

    )


    S.os_scale_y = bpy.props.BoolProperty(

        default=True

    )


    S.os_scale_z = bpy.props.BoolProperty(

        default=True

    )



def unregister_properties():


    props = (

        "os_replace_type",
        "os_object",
        "os_collection",
        "os_keep",
        "os_rot_x",
        "os_rot_y",
        "os_rot_z",
        "os_scale_min",
        "os_scale_max",
        "os_scale_uniform",
        "os_scale_x",
        "os_scale_y",
        "os_scale_z"

    )


    for p in props:

        if hasattr(
            bpy.types.Scene,
            p
        ):

            delattr(
                bpy.types.Scene,
                p
            )





# ============================================================
# SELECT SIMILAR BY NAME
# ============================================================


class OS_OT_select_similar(
        bpy.types.Operator):


    bl_idname = "os.select_similar"

    bl_label = "Select Similar"

    bl_options = {"UNDO"}



    def execute(
            self,
            context):


        active = context.object


        if not active:

            return {"CANCELLED"}



        target = base_name(
            active.name
        )


        result = []



        for o in context.scene.objects:


            if base_name(o.name) == target:

                result.append(o)



        deselect()


        select(result)



        if result:

            context.view_layer.objects.active = result[0]



        return {"FINISHED"}
# ============================================================
# REPLACE
# ============================================================


class OS_OT_replace(
        bpy.types.Operator):


    bl_idname = "os.replace"

    bl_label = "Replace Objects"

    bl_options = {"UNDO"}



    def execute(
            self,
            context):


        scene = context.scene


        old_objects = selected()



        if not old_objects:

            return {"CANCELLED"}



        if scene.os_replace_type == "OBJECT":


            donors = [

                scene.os_object

            ]


        else:


            donors = [

                o for o in scene.os_collection.objects

                if o.type not in {
                    "LIGHT",
                    "CAMERA"
                }

            ]



        if not donors:

            return {"CANCELLED"}



        created = []



        for old in old_objects:


            donor = choice(
                donors
            )



            loc = old.location.copy()

            rot = old.rotation_euler.copy()

            scl = old.scale.copy()



            new = make_copy(

                donor,

                old.users_collection[0]

            )



            new.location = loc

            new.rotation_euler = rot

            new.scale = scl



            created.append(new)



            bpy.data.objects.remove(

                old,

                do_unlink=True

            )




        deselect()

        select(created)



        if created:

            context.view_layer.objects.active = created[0]



        return {"FINISHED"}






# ============================================================
# RANDOM KEEP
# ============================================================


class OS_OT_cull(
        bpy.types.Operator):


    bl_idname = "os.cull"

    bl_label = "Random Keep"

    bl_options = {"UNDO"}



    def execute(
            self,
            context):


        scene = context.scene



        objects = selected()



        if not objects:

            return {"CANCELLED"}




        count = round(

            len(objects)

            *

            scene.os_keep

            /

            100

        )



        count = max(

            1,

            min(

                len(objects),

                count

            )

        )



        result = sample(

            objects,

            count

        )



        deselect()

        select(result)



        if result:

            context.view_layer.objects.active = result[0]



        return {"FINISHED"}






# ============================================================
# RANDOM ROTATION
# ============================================================


class OS_OT_rotation(
        bpy.types.Operator):


    bl_idname = "os.rotation"

    bl_label = "Apply Rotation"

    bl_options = {"UNDO"}



    def execute(
            self,
            context):


        s = context.scene



        for o in selected():


            r = [0,0,0]



            if s.os_rot_x:

                r[0] = radians(
                    uniform(
                        0,
                        360
                    )
                )



            if s.os_rot_y:

                r[1] = radians(
                    uniform(
                        0,
                        360
                    )
                )



            if s.os_rot_z:

                r[2] = radians(
                    uniform(
                        0,
                        360
                    )
                )



            o.rotation_euler.rotate(

                Euler(r)

            )



        return {"FINISHED"}







# ============================================================
# RANDOM SCALE
# ============================================================


class OS_OT_scale(
        bpy.types.Operator):


    bl_idname = "os.scale"

    bl_label = "Apply Scale"

    bl_options = {"UNDO"}



    def execute(
            self,
            context):


        s = context.scene



        for o in selected():


            if s.os_scale_uniform:


                value = uniform(

                    s.os_scale_min,

                    s.os_scale_max

                )


                o.scale *= value



            else:


                if s.os_scale_x:

                    o.scale.x *= uniform(

                        s.os_scale_min,

                        s.os_scale_max

                    )



                if s.os_scale_y:

                    o.scale.y *= uniform(

                        s.os_scale_min,

                        s.os_scale_max

                    )



                if s.os_scale_z:

                    o.scale.z *= uniform(

                        s.os_scale_min,

                        s.os_scale_max

                    )



        return {"FINISHED"}






# ============================================================
# PANEL
# ============================================================


class OS_PT_panel(
        bpy.types.Panel):


    bl_label = "Object Shuffler"


    bl_idname = "OS_PT_panel"


    bl_space_type = "VIEW_3D"


    bl_region_type = "UI"


    bl_category = "Shuffler"




    def draw(
            self,
            context):


        layout = self.layout

        s = context.scene




        box = layout.box()

        box.label(

            text="Object Selection"

        )


        box.operator(

            "os.select_similar",

            text="Select Similar"

        )





        box = layout.box()

        box.label(

            text="Universal Replace"

        )



        box.prop(

            s,

            "os_replace_type",

            expand=True

        )



        if s.os_replace_type == "OBJECT":


            box.prop(

                s,

                "os_object",

                text="Object"

            )



        else:


            box.prop(

                s,

                "os_collection",

                text="Collection"

            )



        box.operator(

            "os.replace",

            text="Replace Objects"

        )






        box = layout.box()

        box.label(

            text="Random Keep"

        )



        box.prop(

            s,

            "os_keep",

            text="Keep %"

        )


        box.operator(

            "os.cull",

            text="Random Keep"

        )







        box = layout.box()

        box.label(

            text="Random Rotation"

        )



        row = box.row(

            align=True

        )


        row.prop(

            s,

            "os_rot_x",

            text="X"

        )


        row.prop(

            s,

            "os_rot_y",

            text="Y"

        )


        row.prop(

            s,

            "os_rot_z",

            text="Z"

        )



        box.operator(

            "os.rotation",

            text="Apply Rotation"

        )






        box = layout.box()

        box.label(

            text="Random Scale"

        )



        row = box.row()



        row.prop(

            s,

            "os_scale_min",