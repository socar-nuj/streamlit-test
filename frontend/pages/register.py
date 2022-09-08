import streamlit as st
from frontend.controller import online_container
from somlier.application.use_cases.online.register.request import RegisterRequest, RegisterRequestV2

use_case = online_container.container.register()
use_case_v2 = online_container.container.register_v2()


st.markdown("## Register Model to MLflow Registry 😎")
st.markdown("""---""")

registration_type = st.radio("Registration Type", ("Model Trained using MLflow", "Pretrained Model (Require GCS URI)"))

if registration_type == "Model Trained using MLflow":
    mlflow_run_id = st.text_input("MLflow Run ID", placeholder="MLflow Run ID를 입력하세요.")
    model_name = st.text_input("Model Name", placeholder="등록하기를 원하는 모델의 이름을 입력하세요.")
    submitted = st.button("Register 🔖", disabled=not mlflow_run_id or not model_name)

    if submitted:
        req = RegisterRequest(run_id=mlflow_run_id, model_name=model_name)
        res = use_case.execute(req)
        st.success(f"{res.message}\n모델 정보: {model_name}/{res.model_version}")

else:
    gcs_artifact_uri = st.text_input("GCS URI for Model Artifact", placeholder="학습된 모델의 아티팩트가 있는 GCS URI를 입력하세요.")
    model_framework_type = st.radio("Model Framework Type", ("scikit-learn", "pytorch"))
    model_name = st.text_input("Model Name", placeholder="등록하기를 원하는 모델의 이름을 입력하세요.")

    if model_framework_type == "scikit-learn":
        project_uri = None
        project_name = None
        project_ref = None
        model_module_path = None
        model_class_name = None
    else:
        project_uri = st.text_input("Project URI", placeholder="모델 클래스 정보가 있는 Github Repository 주소를 입력하세요.")
        project_name = st.text_input("Project Name", placeholder="모델 클래스 정보가 있는 프로젝트 이름을 입력하세요.")
        project_ref = st.text_input("Project Reference", placeholder="모델 클래스 정보가 있는 Github 원격 브랜치 이름을 입력하세요.")
        model_module_path = st.text_input("Model Module Path", placeholder="모델 클래스 정보가 있는 .py 파일의 경로를 입력하세요.")
        model_class_name = st.text_input("Model Class Name", placeholder="모델 클래스 이름을 입력하세요.")

    submitted = st.button("Register 🔖", disabled=not gcs_artifact_uri or not model_name)

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
        st.success(f"{res.message}\n모델 정보: {model_name}/{res.model_version}")
