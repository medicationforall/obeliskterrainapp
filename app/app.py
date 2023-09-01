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
from controls import (
    make_sidebar, 
    make_parameter_controls, 
    make_parameter_controls_layers,
    make_parameter_point,
    make_model_controls,
    make_file_controls
)

def __make_tabs():
    tab_parameters, tab_base, tab_inset, tab_middle, tab_top, tab_overview, tab_layer, tab_file = st.tabs([
        "Parameters",
        "Base",
        "Inset",
        "Middle",
        "Top", 
        "Overview",
        "Layers",
        "File"
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
 
    parameters = model_parameters | base | inset | middle | top | dupe

    with tab_overview:
        st.write(parameters)

    return add_button, parameters, file_controls


def __make_ui():
    if 'models' not in st.session_state:
        st.session_state['models'] = []

    # main ui
    add_button, model_parameters, file_controls = __make_tabs()

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        generate_button = st.button('Generate Model')
    with col2:
        color1 = st.color_picker('Model Color', '#E06600', label_visibility="collapsed")
    with col3:
        render = st.selectbox("Render", ["material", "wireframe"], label_visibility="collapsed")
    
    st.session_state['modified_model_layer'] = False
    make_model_controls(
        model_parameters,
        color1,
        render,
        file_controls
    )

    if add_button:
        # fix dupes
        if len(st.session_state['models']) > 0:
            for model in st.session_state['models']:
                if model_parameters['layer_name']==model['layer_name']:
                    model_parameters['layer_name'] += " copy"
        st.session_state['models'].append(model_parameters)
        st.session_state['modified_model_layer'] = True
        st.experimental_rerun()


if __name__ == "__main__":
    st.set_page_config(
        page_title="CadQuery Box Test",
        page_icon="🧊"
    )
    __make_ui()
    make_sidebar()