import bpy
import json

def import_animation_data(filepath):
    """
    Importe les données d'animation depuis un fichier JSON et applique les transformations à l'armature sélectionnée dans Blender.

    Args:
        filepath (str): Chemin vers le fichier JSON contenant les données d'animation.
    
    Returns:
        None
    """ 

    with open(filepath, 'r') as f:
        animation_data = json.load(f)
    
    # Assurer qu'on est en mode objet
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Sélectionner l'armature
    armature = bpy.context.active_object
    if not armature or armature.type != 'ARMATURE':
        print("Veuillez sélectionner une armature")
        return
    
    # Passer en mode pose
    bpy.ops.object.mode_set(mode='POSE')
    
    # Appliquer les données d'animation
    for frame_data in animation_data:
        frame_num = frame_data["frame"]
        bpy.context.scene.frame_set(frame_num)
        
        for bone_name, bone_data in frame_data["bones"].items():
            if bone_name in armature.pose.bones:
                bone = armature.pose.bones[bone_name]
                bone.location = bone_data["location"]
                bone.keyframe_insert(data_path="location")

# Utilisation dans Blender
# import_animation_data('/path/to/animation_data.json')