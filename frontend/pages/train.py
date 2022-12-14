import pandas as pd
import streamlit as st
from frontend.controller import online_container
from somlier.application.use_cases.online.train.request import TrainRequest


use_case = online_container.container.train()

st.markdown("## Train Model π")
st.markdown("""---""")


@st.experimental_singleton
def get_saved_parameters():
    params = {}
    return params


with st.sidebar:
    st.markdown("### (Optional) Parameters for Model")
    param_name = st.text_input("Parameter Name", placeholder="νλΌλ―Έν°μ μ΄λ¦μ μλ ₯νμΈμ.")
    param_type = st.selectbox("Parameter Type", ("incremental", "discrete"))
    if param_type == "incremental":
        form = st.form(key="increment_form", clear_on_submit=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            param_min_value = form.text_input("Min Value", placeholder="μ°μν λ³μμ μ΅μκ°μ μλ ₯νμΈμ.")
        with c2:
            param_max_value = form.text_input("Max Value", placeholder="μ°μν λ³μμ μ΅λκ°μ μλ ₯νμΈμ.")
        with c3:
            param_increment = form.text_input("Incremental Value", placeholder="μ°μν λ³μμ μ¦κ°ν­μ μλ ₯νμΈμ.")
        param_submitted = form.form_submit_button(label="Add Parameter")

        if param_submitted:
            get_saved_parameters()[param_name] = f"{param_min_value}..{param_max_value}..{param_increment}"
    else:
        form = st.form(key="discrete_form", clear_on_submit=True)
        (c1,) = st.columns(1)
        with c1:
            param_values = form.text_input("Parameter Values", placeholder="κ°μ λ°μ (,)μΌλ‘ κ΅¬λΆν΄ μλ ₯νμΈμ.")

        param_submitted = form.form_submit_button(label="Add Parameter")

        if param_submitted:
            get_saved_parameters()[param_name] = param_values


project_uri = st.text_input("Project URI", placeholder="νμ΅μ μν μ€ν¬λ¦½νΈκ° μλ‘λ λ Github URIλ₯Ό μλ ₯νμΈμ.")
project_name = st.text_input("Project Name", placeholder="νμ΅μ μν μ€ν¬λ¦½νΈκ° μλ‘λ λ νλ‘μ νΈ μ΄λ¦μ μλ ₯νμΈμ.")
project_ref = st.text_input("Project Reference", placeholder="νμ΅μ μν μ€ν¬λ¦½νΈκ° μλ‘λ λ λΈλμΉ μ΄λ¦μ μλ ₯νμΈμ.")

st.write("Parameters Information ")
st.dataframe(pd.DataFrame.from_dict(get_saved_parameters(), orient="index", columns=["parameter values"]))

use_gpu = st.radio("Instance Type", ("CPU", "GPU")) == "GPU"
use_k8s_job = st.radio("Training Environment", ("Local Machine", "Kubernetes")) == "Kubernetes"

c1, c2 = st.columns([2, 1])
with c1:
    submitted = st.button("Train Model π", disabled=not project_uri or not project_name or not project_ref)
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
    st.success(f"λͺ¨λΈ νμ΅μ΄ μ±κ³΅μ μΌλ‘ μ§νλμμ΅λλ€.")
    for run in res:
        st.success(f"MLflow Run ID: {run.run_id}")
if clear_cache:
    get_saved_parameters.clear()
