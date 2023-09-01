# Copyright 2023 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import cadquery as cq
from cqterrain import obelisk

def __make_model_layer(parameters):
    model = obelisk(
        base_width=parameters['base_width'],
        base_height=parameters['base_height'],
        inset_width=parameters['inset_width'],
        inset_height=parameters['inset_height'],
        mid_width=parameters['middle_width'],
        mid_height=parameters['middle_height'],
        top_width=parameters['top_width'],
        top_height=parameters['top_height'],
        height=parameters['height'],
        faces=parameters['faces'],
        intersect=parameters['intersect']
    ).rotate((0,0,1),(0,0,0),parameters['layer_rotate'])

    #__generate_preview_image(model, parameters['layer_name']+'.svg')
    return model

def __generate_preview_image(model, image_name, color1='#E06600', color2='#985926'):
    #create the preview image
    hex_1 = color1.lstrip('#')
    rgb_1 = tuple(int(hex_1[i:i+2], 16) for i in (0, 2, 4))

    hex_2 = color2.lstrip('#')
    rgb_2 = tuple(int(hex_2[i:i+2], 16) for i in (0, 2, 4))
    cq.exporters.export(model, image_name, opt={
        "width": 500,
        "height": 400,
        "marginTop":0,
        "projectionDir": (1, 1, 0.5),
        "showAxes": True,
        "focus": 90,
        "strokeColor": rgb_1,
        "hiddenColor": rgb_2
    })

def __delete_layer(index, name=None):
    if name == st.session_state['models'][index]['layer_name']:
        st.session_state['models'].pop(index)
        st.session_state['modified_model_layer'] = True

def __rotate_layer(index, name=None, key=None):
    rotation_value = st.session_state[key]
    if name == st.session_state['models'][index]['layer_name']:
        st.session_state['models'][index]['layer_rotate'] = rotation_value
        

def make_parameter_controls_layers():
    col1, col2, col3 = st.columns(3)
   
    with col1:
        layer_name = st.text_input("Key Name",f"Layer {len(st.session_state['models'])}")
    with col2:
        layer_rotate = st.number_input("Rotation", min_value=0, max_value=360, step=1, value=0)
    with col3:
        add_button = st.button('➕ Add Model', type="secondary")

    st.subheader("Layers")

    col_name, col_rotation, col_preview, col_details, col_delete = st.columns(5)
    with col_name:
        st.write('Name')
    with col_rotation:
        st.write('Rotation')
    with col_preview:
        st.write('Preview')
    with col_delete:
        st.write('Delete')
        
    for index,layer_params in enumerate(st.session_state['models']):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write(layer_params['layer_name'])
        with col2:
            layer_rotate_custom = st.number_input(
                "Layer Rotate",
                key=f"rotate {layer_params['layer_name']}", 
                label_visibility="collapsed", 
                min_value=0, 
                max_value=360, 
                step=1, 
                value=layer_params['layer_rotate'],
                args=(index, layer_params['layer_name'], f"rotate {layer_params['layer_name']}"), 
                on_change=__rotate_layer
            )
        with col3:
            # make the model generate the image
            model = __make_model_layer(layer_params).rotate((0,1,0),(0,0,0),180)
            __generate_preview_image(model, 'preview.svg')
            # display the image
            st.image('preview.svg')
        with col5:
            st.button(
                "➖",
                key=f"delete {layer_params['layer_name']}",
                args=(index, layer_params['layer_name']), 
                on_click=__delete_layer
                )

    return add_button, {
        'layer_rotate':layer_rotate,
        'layer_name':layer_name
    }