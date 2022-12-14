import streamlit as st
from frontend.controller import online_container
from somlier.application.use_cases.online.register.request import RegisterRequest, RegisterRequestV2

use_case = online_container.container.register()
use_case_v2 = online_container.container.register_v2()


st.markdown("## Register Model to MLflow Registry ð")
st.markdown("""---""")

registration_type = st.radio("Registration Type", ("Model Trained using MLflow", "Pretrained Model (Require GCS URI)"))

if registration_type == "Model Trained using MLflow":
    mlflow_run_id = st.text_input("MLflow Run ID", placeholder="MLflow Run IDë¥¼ ìë ¥íì¸ì.")
    model_name = st.text_input("Model Name", placeholder="ë±ë¡íê¸°ë¥¼ ìíë ëª¨ë¸ì ì´ë¦ì ìë ¥íì¸ì.")
    submitted = st.button("Register ð", disabled=not mlflow_run_id or not model_name)

    if submitted:
        req = RegisterRequest(run_id=mlflow_run_id, model_name=model_name)
        res = use_case.execute(req)
        st.success(f"{res.message}\nëª¨ë¸ ì ë³´: {model_name}/{res.model_version}")

else:
    gcs_artifact_uri = st.text_input("GCS URI for Model Artifact", placeholder="íìµë ëª¨ë¸ì ìí°í©í¸ê° ìë GCS URIë¥¼ ìë ¥íì¸ì.")
    model_framework_type = st.radio("Model Framework Type", ("scikit-learn", "pytorch"))
    model_name = st.text_input("Model Name", placeholder="ë±ë¡íê¸°ë¥¼ ìíë ëª¨ë¸ì ì´ë¦ì ìë ¥íì¸ì.")

    if model_framework_type == "scikit-learn":
        project_uri = None
        project_name = None
        project_ref = None
        model_module_path = None
        model_class_name = None
    else:
        project_uri = st.text_input("Project URI", placeholder="ëª¨ë¸ í´ëì¤ ì ë³´ê° ìë Github Repository ì£¼ìë¥¼ ìë ¥íì¸ì.")
        project_name = st.text_input("Project Name", placeholder="ëª¨ë¸ í´ëì¤ ì ë³´ê° ìë íë¡ì í¸ ì´ë¦ì ìë ¥íì¸ì.")
        project_ref = st.text_input("Project Reference", placeholder="ëª¨ë¸ í´ëì¤ ì ë³´ê° ìë Github ìê²© ë¸ëì¹ ì´ë¦ì ìë ¥íì¸ì.")
        model_module_path = st.text_input("Model Module Path", placeholder="ëª¨ë¸ í´ëì¤ ì ë³´ê° ìë .py íì¼ì ê²½ë¡ë¥¼ ìë ¥íì¸ì.")
        model_class_name = st.text_input("Model Class Name", placeholder="ëª¨ë¸ í´ëì¤ ì´ë¦ì ìë ¥íì¸ì.")

    submitted = st.button("Register ð", disabled=not gcs_artifact_uri or not model_name)

    if submitted:
        req = RegisterRequestV2(
            model_type=model_framework_type,
            gcs_uri=gcs_artifact_uri,
            model_name=model_name,
            project_uri=project_uri,
            project_name=project_name,
            project_ref=project_ref,
            model_module_path=model_module_path,
            model_class_name=model_class_name,
        )
        res = use_case_v2.execute(req)
        st.success(f"{res.message}\nëª¨ë¸ ì ë³´: {model_name}/{res.model_version}")
