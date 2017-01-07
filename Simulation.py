import bpy
import os
import csv
import math
from math import pi

def delete_objects():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern="Planet-*")
    bpy.ops.object.select_pattern(pattern="Orbit-*")
    bpy.ops.object.select_pattern(pattern="Camera-*")
    n = len(bpy.context.selected_objects)
    bpy.ops.object.delete()

    print("%d objects(s) were deleted." % n)

    return


def delete_unused_materials():
    i = 0
    for mat in bpy.data.materials:
        if mat.users == 0:
            name = mat.name
            bpy.data.materials.remove(mat)
            i = i + 1
            print("Deleted material ", name)

    print("%d materials were deleted." % i)

    return


def delete_unused_textures():
    i = 0
    for tex in bpy.data.textures:
        if tex.users == 0:
            name = tex.name
            bpy.data.textures.remove(tex)
            i = i + 1
            print("Deleted texture ", name)
            
    print("%d textures were deleted." % i)
    
    return


def add_texture(mat, imgname):
    
    # Bild oder Textur hinzufügen
    img = bpy.data.images.load(imgname)
    tex = bpy.data.textures.new(imgname, type='IMAGE')
    tex.image = img
    
    mtex = mat.texture_slots.add()
    mtex.texture = tex
    mtex.texture_coords = 'ORCO'
    mtex.mapping = 'SPHERE' 

    return


def add_material(obj, name, color):
    
    # Material erzeugen und hinzufügen
    matname = "Material-" + name
    mat = bpy.data.materials.new(matname)
    mat.diffuse_color = color
    mat.specular_intensity = 0.1

    obj.data.materials.append(mat)

    return mat


def add_orbit(name,apoapsis,smja,smia,duration,inclination):
    bpy.ops.curve.primitive_bezier_circle_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
    
    bpy.ops.transform.resize(value = (smia, smja, 1), constraint_axis = (True, True, False), 
    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', 
    proportional_edit_falloff='SMOOTH', proportional_size=1)
    
    bpy.ops.transform.translate(value=(0,apoapsis-smja,0), constraint_axis=(False, True, False), 
    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', 
    proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)
    
    bpy.ops.transform.rotate(value=argument_of_periapsis, axis=(0.0, 0.0, 1.0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1.0, snap=False, snap_target='CLOSEST', snap_point=(0.0, 0.0, 0.0), snap_align=False, snap_normal=(0.0, 0.0, 0.0), gpencil_strokes=False, release_confirm=False)
    
    bpy.ops.transform.rotate(value=inclination, axis=(0.0, 0.0, 0.0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1.0, snap=False, snap_target='CLOSEST', snap_point=(0.0, 0.0, 0.0), snap_align=False, snap_normal=(0.0, 0.0, 0.0), gpencil_strokes=False, release_confirm=False)
    
    bpy.ops.transform.rotate(value=ascending_node, axis=(0.0, 0.0, 1.0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1.0, snap=False, snap_target='CLOSEST', snap_point=(0.0, 0.0, 0.0), snap_align=False, snap_normal=(0.0, 0.0, 0.0), gpencil_strokes=False, release_confirm=False)
    
    obj = bpy.context.object
    obj.name = name
    
    obj.data.path_duration = duration

    
    
def add_sphere(name, size):
    # Planeten hinzufügen
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=48, ring_count=24, size=size)
    name_orbit = "Orbit-" + name   
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.shade_smooth()
    
    obj.select = True
    
    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
    obj.constraints["Follow Path"].target = bpy.data.objects["Orbit-"+name]
    override={'constraint':obj.constraints["Follow Path"]}
    bpy.ops.constraint.followpath_path_animate(override, constraint="Follow Path", owner='OBJECT')
    bpy.ops.object.location_clear(clear_delta=False)
    
    
    bpy.data.objects[name].constraints["Follow Path"].offset = duration*true_anomaly
       
    print("Sphere '%s' created." % name)
   
    return obj

def add_cam():
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0,0,0), rotation = (pi*3/2,0,pi*1/2))   
    obj = bpy.context.object
    obj.name = "Camera-Earth"
    
    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
    obj.constraints["Follow Path"].target = bpy.data.objects["Orbit-Planet-Earth"]
    override={'constraint':obj.constraints["Follow Path"]}
    bpy.ops.constraint.followpath_path_animate(override, constraint="Follow Path", owner='OBJECT')
    bpy.ops.object.location_clear(clear_delta=False)
    
    bpy.ops.transform.translate(value=(Planets[3][1]/2,0,-0.1), constraint_axis=(True, False, True), 
    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', 
    proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)

    bpy.data.objects["Camera-Earth"].constraints["Follow Path"].offset = Planets[3][6]*1000*Planets[3][10]/360    
   
    
if __name__ == '__main__':
    
    # Planeten und Texturen löschen
    
    delete_objects()
    delete_unused_materials()
    delete_unused_textures()
    
    #import von daten
    cam = True 
    Planets = []
    
    filepath = bpy.path.abspath("//planets3.csv")
    csvfile = open(filepath, 'r', newline = '')
    ofile = csv.reader(csvfile, delimiter=',')
    
    for i, row in enumerate(ofile):
        if (i > 0):
            Planets.append([row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), [float(row[5]), float(row[6]), float(row[7])], float(row[8]), float(row[9]),float(row[10]), float(row[11]), float(row[12])])
        
    csvfile.close()
    
    for p in Planets:
        # loop für das ganze System

        
        # Hinzufügen von Planeten
        name = p[0]
        size = p[1]
        size_factor = 3
        apoapsis = p[2]*size_factor
        periapsis = p[3]*size_factor
        smja = size_factor*(p[3]+p[2])/2
        #smja=Breite Achse
        smia = size_factor*p[3]*(1-p[4]**2)**(1/2)
        #smia=Schmale Achse
        color = p[5]
        duration = p[6]*1000
        inclination = p[7]/180*pi
        argument_of_periapsis = p[8]/180*pi
        ascending_node = p[9]/180*pi
        true_anomaly = p[10]/360
        
        
        #Bogenmass
            
        location = [0,0,0]
        objname = "Planet-" + name
        objname_orbit = "Orbit-" + objname

        obj_orbit = add_orbit(objname_orbit, apoapsis, smja, smia, duration, inclination)
        
        obj = add_sphere(objname, size)
        
        # add a material to the object
        mat = add_material(obj, name, color)
        
    if cam == True:
        add_cam()
