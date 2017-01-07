import bpy
import os
import csv
import math

def delete_planets():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern="Planet-*")
    n = len(bpy.context.selected_objects)
    bpy.ops.object.delete()

    print("%d planet(s) were deleted." % n)

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


def add_material(obj, name):
    
    # Material erzeugen und hinzufügen
    matname = "Material-" + name
    mat = bpy.data.materials.new(matname)
    mat.diffuse_color = [0,0,1]
    mat.specular_intensity = 0.1

    obj.data.materials.append(mat)

    return mat


def add_sphere(name, location):
   
    # Planeten hinzufügen
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=48, ring_count=24, size=1.0,
        location=location, rotation=[0,0,0])
    
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.shade_smooth()
       
    print("Sphere '%s' created." % name)
   
    return obj
 

if __name__ == '__main__':

    # Csv-Datei mit Planetinfos

    with open('planets.csv') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=',')

      lines = [r for r in reader if not r[reader.fieldnames[0]].startswith("#")]
    print(lines[0]["name"])
    # Planeten und Texturen löschen
    #delete_planets()
    #delete_unused_materials()
    #delete_unused_textures()
    
    # Geplanter loop für das ganze System
    #for name, radius, art_distance, flattening, tilt, tilt_x, tilt_y, tilt_z, rotperiod, eccentricity, orbitperoid, texture, color in 'planets-list':
     #   print(name)
      #  print(radius)
    # Hinzufügen von Planeten
    #location = [art_distance,0,0]

    #objname = "Planet-" + name

#    obj = add_sphere(objname, location)
    
    # add a material to the object
 #   mat = add_material(obj, name)
    
    # Orbitale   
    # (Ringe für Saturn)
        
    # loop-endez
