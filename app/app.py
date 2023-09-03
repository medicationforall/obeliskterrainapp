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

#--------------------  

import streamlit as st
from uuid import uuid4
import glob
import time
from datetime import datetime, date
from pathlib import Path
from controls import (
    make_sidebar, 
    make_parameter_controls, 
    make_parameter_controls_layers,
    make_parameter_point,
    make_model_controls,
    make_file_controls
)

def __make_tabs():
    tab_parameters, tab_base, tab_inset, tab_middle, tab_top, tab_layer, tab_file, tab_overview = st.tabs([
        "Model",
        "Base",
        "Inset",
        "Middle",
        "Top", 
        "Layers",
        "File",
        "Overview",
        ])
    with tab_parameters:
        model_parameters = make_parameter_controls()
    with tab_base:
        base = make_parameter_point('base', 3.0, 30.0)
    with tab_inset:
        inset = make_parameter_point('inset', 5.0, 15.0)
    with tab_middle:
        middle = make_parameter_point('middle', 15.0, 30.0)
    with tab_top:
        top = make_parameter_point('top', 70.0, 15.0)
    with tab_layer:
        add_button, dupe = make_parameter_controls_layers()
    with tab_file:
        file_controls = make_file_controls()
 
    #combine tab parameter into one dictionary
    parameters = model_parameters | base | inset | middle | top | dupe

    with tab_overview:
        col1,col2 = st.columns(2)
        with col1:
            st.write("Current")
        with col2:
            st.write("Layers")

        col1,col2 = st.columns(2)
        with col1:
            st.write(parameters)
        with col2:
            st.write(st.session_state['models'])

    return add_button, parameters, file_controls

def __initialize_session():
    if 'models' not in st.session_state:
        st.session_state['models'] = []

    if "session_id" not in st.session_state:
        st.session_state['session_id'] = uuid4()


def __model_controls(model_parameters, file_controls):
    col1, col2, col3 = st.columns(3)
    with col1:
        generate_button = st.button('Generate Model')
    with col2:
        color1 = st.color_picker('Model Color', '#E06600', label_visibility="collapsed")
    with col3:
        render = st.selectbox("Render", ["material", "wireframe"], label_visibility="collapsed")

    make_model_controls(
        model_parameters,
        color1,
        render,
        file_controls
    )

def __handle_add_button_click(add_model_layer_button):
    if add_model_layer_button:
        # fix layer name dupes
        if len(st.session_state['models']) > 0:
            for model in st.session_state['models']:
                if model_parameters['layer_name']==model['layer_name']:
                    model_parameters['layer_name'] += " copy"

        st.session_state['models'].append(model_parameters)
        st.experimental_rerun()

def __make_app():
    # main tabs
    add_model_layer_button, model_parameters, file_controls = __make_tabs()
    st.divider()
    __model_controls(model_parameters, file_controls)
    __handle_add_button_click(add_model_layer_button)


def __clean_up_static_files():
    files = glob.glob("app/static/model_*.stl")
    today = datetime.today()
    #print(files)
    for file_name in files:
        file_path = Path(file_name)
        modified = file_path.stat().st_mtime
        modified_date = datetime.fromtimestamp(modified)
        delta = today - modified_date
        #print('total seconds '+str(delta.total_seconds()))
        if delta.total_seconds() > 1200: # 20 minutes
            #print('removing '+file_name)
            file_path.unlink()


if __name__ == "__main__":
    st.set_page_config(
        page_title="CadQuery Obelisk Generator",
        page_icon="🧊"
    )
    __initialize_session()
    __make_app()
    make_sidebar()
    __clean_up_static_files()