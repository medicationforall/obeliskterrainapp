import streamlit as st

def __make_scene(models):
    unions = ''

    scene_begin = f'''
scene = (
    cq.Workplane("XY")
    .union(model)
'''

    for index, params in enumerate(models):
        if params["layer_display"]:
            scene_begin = scene_begin + f'''    .union(model_{index})
'''
    return scene_begin +unions+ ')'

def __make_layer_code(index, parameters):
    base_width = parameters['base_width']
    base_height = parameters['base_height']
    inset_width = parameters['inset_width']
    inset_height = parameters['inset_height']
    middle_width = parameters['middle_width']
    middle_height = parameters['middle_height']
    top_width = parameters['top_width']
    top_height = parameters['top_height']
    height = parameters['height']
    faces = parameters['faces']
    intersect = parameters['intersect']
    layer_rotate = parameters['layer_rotate']
    layer_name = parameters['layer_name']

    layer_string = f'''
# {layer_name}
model_{index} = obelisk(
        base_width={base_width},
        base_height={base_height},
        inset_width={inset_width},
        inset_height={inset_height},
        mid_width={middle_width},
        mid_height={middle_height},
        top_width={top_width},
        top_height={top_height},
        height={height},
        faces={faces},
        intersect={intersect}
    ).rotate((0,0,1),(0,0,0),{layer_rotate})

'''
    return layer_string

def make_code_view(parameters, models):
    base_width = parameters['base_width']
    base_height = parameters['base_height']
    inset_width = parameters['inset_width']
    inset_height = parameters['inset_height']
    middle_width = parameters['middle_width']
    middle_height = parameters['middle_height']
    top_width = parameters['top_width']
    top_height = parameters['top_height']
    height = parameters['height']
    faces = parameters['faces']
    intersect = parameters['intersect']
    layer_rotate = parameters['layer_rotate']

    code_string = f'''
import cadquery as cq
from cqterrain import obelisk

model = obelisk(
        base_width={base_width},
        base_height={base_height},
        inset_width={inset_width},
        inset_height={inset_height},
        mid_width={middle_width},
        mid_height={middle_height},
        top_width={top_width},
        top_height={top_height},
        height={height},
        faces={faces},
        intersect={intersect}
    ).rotate((0,0,1),(0,0,0),{layer_rotate})

'''

    if len(models) > 0:
        for index, layer_params in enumerate(models):
            layer_string = __make_layer_code(index, layer_params)
            code_string = code_string + layer_string


    code_string = code_string + __make_scene(models)

    code_string = code_string + '''
show_object(scene)
# cq.exporters.export(scene, 'obelisk.stl')
'''


    st.code(
    f'{code_string}',
    language="python", 
    line_numbers=True
)