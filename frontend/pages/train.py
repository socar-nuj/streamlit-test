import pandas as pd
import streamlit as st
from frontend.controller import online_container
from somlier.application.use_cases.online.train.request import TrainRequest


use_case = online_container.container.train()

st.markdown("## Train Model 😎")
st.markdown("""---""")


@st.experimental_singleton
def get_saved_parameters():
    params = {}
    return params


with st.sidebar:
    st.markdown("### (Optional) Parameters for Model")
    param_name = st.text_input("Parameter Name", placeholder="파라미터의 이름을 입력하세요.")
    param_type = st.selectbox("Parameter Type", ("incremental", "discrete"))
    if param_type == "incremental":
        form = st.form(key="increment_form", clear_on_submit=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            param_min_value = form.text_input("Min Value", placeholder="연속형 변수의 최솟값을 입력하세요.")
        with c2:
            param_max_value = form.text_input("Max Value", placeholder="연속형 변수의 최댓값을 입력하세요.")
        with c3:
            param_increment = form.text_input("Incremental Value", placeholder="연속형 변수의 증가폭을 입력하세요.")
        param_submitted = form.form_submit_button(label="Add Parameter")

        if param_submitted:
            get_saved_parameters()[param_name] = f"{param_min_value}..{param_max_value}..{param_increment}"
    else:
        form = st.form(key="discrete_form", clear_on_submit=True)
        (c1,) = st.columns(1)
        with c1:
            param_values = form.text_input("Parameter Values", placeholder="값을 반점(,)으로 구분해 입력하세요.")

        param_submitted = form.form_submit_button(label="Add Parameter")

        if param_submitted:
            get_saved_parameters()[param_name] = param_values


project_uri = st.text_input("Project URI", placeholder="학습을 위한 스크립트가 업로드 된 Github URI를 입력하세요.")
project_name = st.text_input("Project Name", placeholder="학습을 위한 스크립트가 업로드 된 프로젝트 이름을 입력하세요.")
project_ref = st.text_input("Project Reference", placeholder="학습을 위한 스크립트가 업로드 된 브랜치 이름을 입력하세요.")

st.write("Parameters Information ")
st.dataframe(pd.DataFrame.from_dict(get_saved_parameters(), orient="index", columns=["parameter values"]))

use_gpu = st.radio("Instance Type", ("CPU", "GPU")) == "GPU"
use_k8s_job = st.radio("Training Environment", ("Local Machine", "Kubernetes")) == "Kubernetes"

c1, c2 = st.columns([2, 1])
with c1:
    submitted = st.button("Train Model 🔖", disabled=not project_uri or not project_name or not project_ref)
with c2:
    clear_cache = st.button("Initialize Parameters History")

if submitted:
    req = TrainRequest(
        project_uri=project_uri,
        project_name=project_name,
        project_version=project_ref,
        use_k8s_job=use_k8s_job,
        use_gpu=use_gpu,
        params=get_saved_parameters(),
    )
    res = use_case.execute(req)
    st.success(f"모델 학습이 성공적으로 진행되었습니다.")
    for run in res:
        st.success(f"MLflow Run ID: {run.run_id}")
if clear_cache:
    get_saved_parameters.clear()
