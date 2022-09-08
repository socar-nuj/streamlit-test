import streamlit as st
from frontend.controller import offline_container
from somlier.application.use_cases.offline.create import CreateBatchRequest, CreateBatchRequestV2

use_case = offline_container.container.create()
use_case_v2 = offline_container.container.create_v2()


st.markdown("## Offline Serving (Airflow DAGs) 😎")
st.markdown("""---""")

offline_serving_type = st.radio("Serving Type", ("Use Docker Image", "Use SOCAR Data Provider"))

dag_schedule_interval = st.text_input("DAG Schedule Interval", placeholder="DAG의 실행 주기를 cronjob 표현식으로 입력하세요.")
dag_id = st.text_input("DAG ID", placeholder="DAG ID를 입력하세요. DAG ID는 Unique해야합니다.")

if offline_serving_type == "Use Docker Image":
    docker_image = st.text_input(
        "Docker Image Reference", placeholder="도커 이미지 정보를 입력하세요.", help="e.g., gcr.io/socar-data-dev/sift:latest"
    )
    docker_entrypoint = st.text_input(
        "Docker Container Entrypoint", placeholder="도커 컨테이너의 Entrypoint를 입력하세요.", help="e.g., sh -c predict.sh"
    )

    use_dry_run = st.checkbox("Use Dry Run")
    check_airflow = st.checkbox("Check Airflow DAG Using REST API")

    submitted = st.button(
        "Serve Model 🔖", disabled=not dag_id or not dag_schedule_interval or not docker_image or not docker_entrypoint
    )
    if submitted:
        req = CreateBatchRequest(
            docker_image=docker_image, schedule=dag_schedule_interval, entrypoint=docker_entrypoint, dag_id=dag_id
        )
        res = use_case.execute(req)
        st.success(f"DAG 스크립트 생성이 완료되었습니다.")
        st.download_button("Download DAG Script File", data=res.dag, file_name=f"somlier_offline_dag_{dag_id}.py")


else:
    dag_start_date = st.date_input("DAG Start Date").strftime("%Y-%m-%d")
    mlflow_model_ref = st.text_input(
        "MLflow Model Reference",
        placeholder="MLflow Model Registry에 존재하는 모델 정보를 입력하세요.",
        help="e.g., boston-house-pricing/2",
    )
    dataset_ref = st.text_input(
        "Feature Dataset Table Reference (BigQuery)",
        placeholder="모델의 입력이 될 BigQuery 테이블 정보를 입력하세요.",
        help="e.g., temp_serena.boston_house_pricing_feature_set",
    )
    dataset_load_column = st.text_input(
        "Column Name for Loading Dataset",
        placeholder="인퍼런스 대상의 기준이 되는 컬럼 이름을 입력하세요.",
        help="e.g., date",
    )
    dataset_load_by_kst = (
        st.radio("Column Timezone for Loading Dataset", ("KST(Asia/Seoul')", "UTC")) == "KST(Asia/Seoul')"
    )
    destination_table_ref = st.text_input(
        "Destination Table Reference (BigQuery)",
        placeholder="인퍼런스 결과값이 적재될 BigQuery 테이블 정보를 입력하세요.",
        help="e.g., temp_serena.boston_house_pricing_result",
    )
    github_personal_access_token = st.text_input(
        "Github Personal Access Token",
        type="password",
        placeholder="Pull Request 생성을 위한 Personal Access Token 값",
    )
    submitted = st.button(
        "Serve Model 🔖",
        disabled=not dag_id
        or not dag_schedule_interval
        or not dag_start_date
        or not mlflow_model_ref
        or not dataset_ref
        or not dataset_load_column
        or not destination_table_ref
        or not github_personal_access_token,
    )

    if submitted:
        req = CreateBatchRequestV2(
            model_ref=mlflow_model_ref,
            dag_id=dag_id,
            schedule_interval=dag_schedule_interval,
            start_date=dag_start_date,
            dataset_ref=dataset_ref,
            dataset_load_column=dataset_load_column,
            dataset_load_by_kst=dataset_load_by_kst,
            dataset_load_window=1,
            destination_table_ref=destination_table_ref,
            github_personal_access_token=github_personal_access_token,
        )
        res = use_case_v2.execute(req)
        st.success(f"DAG 생성 및 PR 생성이 완료되었습니다.")
        st.success(res.msg)
