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
from .layersTable import layers_table
  
def make_parameter_controls_layers():
    col1, col2, col3 = st.columns(3)
   
    with col1:
        layer_name = st.text_input("Key Name",f"Layer {len(st.session_state['models'])}")
    with col2:
        layer_rotate = st.number_input("Rotation", min_value=0, max_value=360, step=1, value=0)
    with col3:
        add_button = st.button('➕ Add Model', type="secondary")

    layers_table()

    return add_button, {
        'layer_rotate':layer_rotate,
        'layer_name':layer_name,
        'layer_display':True
    }