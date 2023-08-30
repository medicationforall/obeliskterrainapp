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
    make_parameter_controls_base,
    make_parameter_controls_inset,
    make_parameter_controls_middle,
    make_parameter_controls_top,
    make_model_controls,
    make_file_controls
)

def __make_tabs():
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Parameters","Base","Inset","Middle","Top", "File", "Overview"])
    with tab1:
        model_parameters = make_parameter_controls()
    with tab2:
        base = make_parameter_controls_base()
    with tab3:
        inset = make_parameter_controls_inset()
    with tab4:
        middle = make_parameter_controls_middle()
    with tab5:
        top = make_parameter_controls_top()
    with tab6:
        file_controls = make_file_controls()
 
    parameters = model_parameters | base | inset | middle | top

    with tab7:
        st.write(parameters)

    return parameters, file_controls


def __make_ui():

    if 'key'not in st.session_state:
        st.session_state['key'] = 0
    else:
        st.session_state['key'] = 1

    # main ui
    model_parameters, file_controls = __make_tabs()

    col1, col2, col3 = st.columns(3)
    with col1:
        generate_button = st.button('Generate Model', type="primary")
    with col2:
        color1 = st.color_picker('Model Color', '#E0BD00', label_visibility="collapsed")
    with col3:
        render = st.selectbox("Render", ["material", "wireframe"], label_visibility="collapsed")
    
    if generate_button  or st.session_state['key']==0:
        make_model_controls(
            model_parameters,
            color1,
            render,
            file_controls
        )

        #if st.session_state['key']==1:
        #    st.balloons()
    else:
        st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬆️Please click the \"Generate Model\" Button")


if __name__ == "__main__":
    st.set_page_config(
        page_title="CadQuery Box Test",
        page_icon="🧊"
    )

    #st.title('CadQuery Box Test')
    __make_ui()
    make_sidebar()