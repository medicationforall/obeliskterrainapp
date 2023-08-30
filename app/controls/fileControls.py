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

def make_file_controls():
    col1, col2 = st.columns(2)
    with col1:
        download_name = st.text_input('File Name','model')
    with col2:
        export_type = st.selectbox("File type",('stl','step'))
    return {
        'name':download_name,
        'type':export_type
    }