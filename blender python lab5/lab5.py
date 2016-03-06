import bpy
import math

#http://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Other_data_types
#http://blender.stackexchange.com/questions/6173/where-does-console-output-go
#http://blender.stackexchange.com/questions/14889/how-to-get-an-armature-by-name-in-python-and-get-access-to-its-bones
#http://stackoverflow.com/questions/28622785/rotation-between-keyframes
#http://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Other_data_types
#http://blender.stackexchange.com/questions/6173/where-does-console-output-go
#http://blender.stackexchange.com/questions/14889/how-to-get-an-armature-by-name-in-python-and-get-access-to-its-bones
#http://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Other_data_types
#http://blender.stackexchange.com/questions/6173/where-does-console-output-go
#http://blender.stackexchange.com/questions/14889/how-to-get-an-armature-by-name-in-python-and-get-access-to-its-bones
#http://blender.stackexchange.com/questions/8387/how-to-get-keyframe-data-from-python
#http://blender.stackexchange.com/questions/5636/how-can-i-get-the-location-of-an-object-at-each-keyframe
#http://stackoverflow.com/questions/8865672/how-to-move-a-camera-in-blender-2-61-with-python
#http://blender.stackexchange.com/questions/32805/rotate-an-object-around-an-axis-using-python-script
#http://stackoverflow.com/questions/8865672/how-to-move-a-camera-in-blender-2-61-with-python
#http://blender.stackexchange.com/questions/5636/how-can-i-get-the-location-of-an-object-at-each-keyframe
#https://www.reddit.com/r/blender/comments/1gc8od/is_there_a_way_to_link_the_scale_of_an/?
#http://blender.stackexchange.com/questions/8387/how-to-get-keyframe-data-from-python
#http://blender.stackexchange.com/questions/3476/how-can-i-animate-the-camera-in-a-perfect-circular-rotation-around-a-fixed-posit
#http://blender.stackexchange.com/questions/1311/how-can-i-get-vertex-positions-from-a-mesh

scn = bpy.context.scene
for ob in scn.objects:
    if ob.name == 'rot_cam':
        ob.select = True
        bpy.ops.object.delete()


bpy.ops.object.add(type="CAMERA")
cam = bpy.context.object
cam.name = "rot_cam"

scene = bpy.context.scene

bpy.ops.object.empty_add()
target = bpy.context.active_object
target.name = 'focus point'
target.location = bpy.data.objects['131_09_60fps'].location
cam.parent = target

cam.location[0] = 5
cam.location[1] = 5
cam.location[2] = 0


tc = cam.constraints.new(type='TRACK_TO')
tc.target = target
tc.subtarget = "Head"
tc.up_axis = 'UP_Y'
tc.track_axis = 'TRACK_NEGATIVE_Z'


scene.frame_current = 1
target.rotation_euler = (0,0,0)
target.keyframe_insert(data_path="rotation_euler")
scene.frame_current = 1147
target.rotation_euler = (0,0,math.radians(360))
target.keyframe_insert(data_path="rotation_euler")

for fc in target.animation_data.action.fcurves:
    fc.extrapolation = 'LINEAR'
    for kp in fc.keyframe_points:
        kp.interpolation = 'LINEAR'


bpy.ops.object.constraint_add(type='COPY_LOCATION')
bpy.context.object.constraints["Copy Location"].target = bpy.data.objects["131_09_60fps"]
bpy.context.object.constraints["Copy Location"].subtarget = "Head"
