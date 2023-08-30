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

def make_parameter_controls():
    col1, col2, col3 = st.columns(3)
    with col1:
        height = st.number_input("height",min_value=1.0, value=110.0,step=1.0)
    with col2:
        faces = st.number_input("faces",min_value=2, max_value=30,  value=4,step=1)
    with col3:
        intersect = st.checkbox("Intersect", True)

    return {
        'height':height,
        'faces':faces,
        'intersect':intersect
    }