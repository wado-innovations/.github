import bpy

# Sélectionne le mesh
obj = bpy.data.objects['profile aile et cloison']
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Edit mode → séparer par matériau
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='MATERIAL')
bpy.ops.object.mode_set(mode='OBJECT')