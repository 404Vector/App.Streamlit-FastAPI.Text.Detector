import streamlit as st
from random import randint
import requests
import cv2
import numpy as np

# set state
def init_state_key(key:str, value) -> None:
    if key not in st.session_state:
        st.session_state[key] = value

init_state_key('api_ocr','http://localhost:30002/ocr-detection')
init_state_key('title', "글자 영역 검출 Service")
init_state_key('description', "사용자가 업로드한 이미지에서 글자영역을 검출하고, BBox를 그려서 반환해줍니다.")
init_state_key('file', str(randint(1000, 100000000)))
init_state_key('complete_pred', False)
init_state_key('uploaded_file', None)
init_state_key('result_image', None)

# set events
def on_reset_btn_clicked():
    st.session_state.result_image = None
    st.session_state.complete_pred = False

def on_excute_btn_clicked():
    if st.session_state.uploaded_file == None : return
    response = requests.post(st.session_state.api_ocr, files = st.session_state.uploaded_file)
    st.session_state.result_image = response.content
    st.session_state.complete_pred = True

# set page view
st.set_page_config(page_title = st.session_state['title'],
                   layout = "centered",
                   initial_sidebar_state = "expanded"
                )

st.title(st.session_state['title'])
st.text(st.session_state['description'])

### Columns
layout_upload, layout_control = st.columns([2,0.5])

with layout_upload:
    uploaded_file = st.file_uploader(".", type=["jpg", "jpeg", "png"],
                                    label_visibility = "collapsed",
                                    accept_multiple_files=False)
    if uploaded_file is not None:
        st.session_state.uploaded_file = {'files':uploaded_file.getvalue()}#('file', (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type))
        
with layout_control:
    st.button('Excute', on_click=on_excute_btn_clicked, type="primary")
    st.button('Reset', on_click=on_reset_btn_clicked, type="primary")

result_placeholder = st.empty() if st.session_state.result_image == None else st.image(st.session_state.result_image)

st.text("Created by 김형석B-T4063@boostcamp AI Tech 4th")