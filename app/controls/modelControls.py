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
import streamlit.components.v1 as components
import cadquery as cq
from cqterrain import obelisk
import os
import time


EXPORT_NAME = 'model'
PREVIEW_NAME = 'preview.svg'

def __generate_model(parameters):
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
    )

    #if parameters['duplicate']:
    #    scene = (
    #        cq.Workplane("XY")
    #        .union(model)
    #        .union(model.rotate((0,0,1),(0,0,0), parameters['duplicate_rotate']))
    #    )

    #    return scene
    #else:
    return model

def __generate_preview_image(model, image_name, camera):
    #create the preview image
    hex_1 = color1.lstrip('#')
    rgb_1 = tuple(int(hex_1[i:i+2], 16) for i in (0, 2, 4))

    hex_2 = color2.lstrip('#')
    rgb_2 = tuple(int(hex_2[i:i+2], 16) for i in (0, 2, 4))
    cq.exporters.export(model, image_name, opt={
        "projectionDir": (camera['axis1'], camera['axis2'], camera['axis3']),
        "showAxes": True,
        "focus": camera['focus'],
        "strokeColor": rgb_1,
        "hiddenColor": rgb_2
    })

def __stl_preview(color, render):
    # Load and embed the JavaScript file
    with open("js/three.min.js", "r") as js_file:
        three_js = js_file.read()

    with open("js/STLLoader.js", "r") as js_file:
        stl_loader = js_file.read()

    with open("js/OrbitControls.js", "r") as js_file:
        orbital_controls = js_file.read()

    with open("js/stl-viewer.js", "r") as js_file:
        stl_viewer_component = (
            js_file.read()
            .replace('{__REPLACE_COLOR__}',f'0x{color[1:]}')
            .replace('{__REPLACE_MATERIAL__}',render)
        )
        


    components.html(
        r'<div style="height:500px">'+
        r'<script>'+
        three_js+' '+
        stl_loader+' '+
        orbital_controls+' '+
        'console.log(\'frizzle\');'+
        stl_viewer_component+' '+
        r'</script>'+
        r'<stl-viewer model="./app/static/model.stl?cache='+str(time.time())+r'"></stl-viewer>'+
        r'</div>',
        height = 500
    )


def make_model_controls(
    parameters,
    color,
    render,
    file_controls
):
    start = time.time()
    with st.spinner('Generating Model..'):
        download_name = file_controls['name']
        export_type = file_controls['type'] 
        model = __generate_model(parameters)

        #create the model file for downloading
        cq.exporters.export(model,f'{EXPORT_NAME}.{export_type}')
        cq.exporters.export(model,'app/static/'+f'{EXPORT_NAME}.stl')
        #__generate_preview_image(model, PREVIEW_NAME, color1, color2, camera)
        

        end = time.time()

        #st.write("Preview:")
        __stl_preview(color, render)
        #st.image(PREVIEW_NAME)

        if f'{EXPORT_NAME}.{export_type}' not in os.listdir():
            st.error('The program was not able to generate the mesh.', icon="🚨")
        else:
            with open(f'{EXPORT_NAME}.{export_type}', "rb") as file:
                btn = st.download_button(
                        label=f"Download {export_type}",
                        data=file,
                        file_name=f'{download_name}.{export_type}',
                        mime=f"model/{export_type}"
                    )
                    
            st.success(f'Rendered in {int(end-start)} seconds', icon="✅")