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

def layers_table():
    st.subheader("Layers")
    __layers_table_header()

    for index, layer_params in enumerate(st.session_state['models']):
        __layers_table_row(index, layer_params)
        
def __layers_table_header():
    columns = ['Display', 'Preview', 'Name', 'Rotation', 'Delete']
    for index, tab in enumerate(st.columns(len(columns))):
        with tab:
            st.write(columns[index])

def __layers_table_row(index, layer_params):
    col_display, col_preview, col_name, col_rotation, col_delete = st.columns(5)
    with col_display:
        __display_control(index, layer_params)
    with col_name:
        st.write(layer_params['layer_name'])
    with col_rotation:
        __row_rotate_control(index, layer_params)
    with col_preview:
        __preview_image(layer_params)
    with col_delete:
        __row_delete_button(index, layer_params)

def __display_control(index, layer_params):
    st.checkbox(
        'Display',
        key = f"display {layer_params['layer_name']}", 
        label_visibility = "collapsed", 
        value = layer_params['layer_display'],
        args = (index,), 
        on_change = __display_layer_event
    )

def __display_layer_event(index):
    st.session_state['models'][index]['layer_display'] = not st.session_state['models'][index]['layer_display']
    st.session_state['modified_model_layer'] = True

def __preview_image(layer_params):
        model = __make_model_layer(layer_params).rotate((0,1,0),(0,0,0),180)
        __generate_preview_image(model, 'preview.svg')
        st.image('preview.svg')

def __row_rotate_control(index, layer_params):
        st.number_input(
            "Layer Rotate",
            key = f"rotate {layer_params['layer_name']}", 
            label_visibility = "collapsed", 
            min_value = 0, 
            max_value = 360, 
            step = 1, 
            value = layer_params['layer_rotate'],
            args = (index, layer_params['layer_name'], f"rotate {layer_params['layer_name']}"), 
            on_change = __rotate_layer_event
        )

def __rotate_layer_event(index, name=None, key=None):
    rotation_value = st.session_state[key]
    if name == st.session_state['models'][index]['layer_name']:
        st.session_state['models'][index]['layer_rotate'] = rotation_value

def __row_delete_button(index, layer_params):
    st.button(
        "➖",
        key=f"delete {layer_params['layer_name']}",
        args=(index, layer_params['layer_name']), 
        on_click=__delete_layer_event
        )

def __delete_layer_event(index, name=None):
    if name == st.session_state['models'][index]['layer_name']:
        st.session_state['models'].pop(index)
        st.session_state['modified_model_layer'] = True

def __make_model_layer(parameters):
    model = obelisk(
        base_width = parameters['base_width'],
        base_height = parameters['base_height'],
        inset_width = parameters['inset_width'],
        inset_height = parameters['inset_height'],
        mid_width = parameters['middle_width'],
        mid_height = parameters['middle_height'],
        top_width = parameters['top_width'],
        top_height = parameters['top_height'],
        height = parameters['height'],
        faces = parameters['faces'],
        intersect = parameters['intersect']
    ).rotate((0,0,1),(0,0,0),parameters['layer_rotate'])
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