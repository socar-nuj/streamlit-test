import streamlit as st
from frontend.controller import online_container
from somlier.application.use_cases.online.deploy import DeployRequest

use_case = online_container.container.deploy()["local"]

st.markdown("## Deploy Model 😎")
st.markdown("""---""")

project_name = st.text_input("MLflow Experiment Name", placeholder="실험이 기록된 MLflow experiment 이름을 입력하세요.")
model_name = st.text_input("Model Name", placeholder="모델의 이름을 입력하세요.")
model_version = st.text_input("Model Version", placeholder="모델의 버전을 입력하세요.")

use_k8s = st.checkbox("Deploy on Kubernetes")
use_gpu = st.checkbox("Use GPU")
istio_enabled = st.checkbox("Enable istio (only for k8s)")

submitted = st.button("Deploy 🔖", disabled=not project_name or not model_name or not model_version)

if submitted:
    req = DeployRequest(
        model_name=model_name,
        model_version=model_version,
        use_k8s=use_k8s,
        use_gpu=use_gpu,
        istio_enabled=istio_enabled,
    )
    res = use_case.execute(req)
    st.success(res)
