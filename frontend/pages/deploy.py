import streamlit as st
from frontend.controller import online_container
from somlier.application.use_cases.online.deploy import DeployRequest

use_case = online_container.container.deploy()["local"]

st.markdown("## Deploy Model π")
st.markdown("""---""")

project_name = st.text_input("MLflow Experiment Name", placeholder="μ€νμ΄ κΈ°λ‘λ MLflow experiment μ΄λ¦μ μλ ₯νμΈμ.")
model_name = st.text_input("Model Name", placeholder="λͺ¨λΈμ μ΄λ¦μ μλ ₯νμΈμ.")
model_version = st.text_input("Model Version", placeholder="λͺ¨λΈμ λ²μ μ μλ ₯νμΈμ.")

use_k8s = st.checkbox("Deploy on Kubernetes")
use_gpu = st.checkbox("Use GPU")
istio_enabled = st.checkbox("Enable istio (only for k8s)")

submitted = st.button("Deploy π", disabled=not project_name or not model_name or not model_version)

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
