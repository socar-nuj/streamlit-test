import streamlit as st
from frontend.controller import offline_container
from somlier.application.use_cases.offline.create import CreateBatchRequest, CreateBatchRequestV2

use_case = offline_container.container.create()
use_case_v2 = offline_container.container.create_v2()


st.markdown("## Offline Serving (Airflow DAGs) ๐")
st.markdown("""---""")

offline_serving_type = st.radio("Serving Type", ("Use Docker Image", "Use SOCAR Data Provider"))

dag_schedule_interval = st.text_input("DAG Schedule Interval", placeholder="DAG์ ์คํ ์ฃผ๊ธฐ๋ฅผ cronjob ํํ์์ผ๋ก ์๋ ฅํ์ธ์.")
dag_id = st.text_input("DAG ID", placeholder="DAG ID๋ฅผ ์๋ ฅํ์ธ์. DAG ID๋ Uniqueํด์ผํฉ๋๋ค.")

if offline_serving_type == "Use Docker Image":
    docker_image = st.text_input(
        "Docker Image Reference", placeholder="๋์ปค ์ด๋ฏธ์ง ์ ๋ณด๋ฅผ ์๋ ฅํ์ธ์.", help="e.g., gcr.io/socar-data-dev/sift:latest"
    )
    docker_entrypoint = st.text_input(
        "Docker Container Entrypoint", placeholder="๋์ปค ์ปจํ์ด๋์ Entrypoint๋ฅผ ์๋ ฅํ์ธ์.", help="e.g., sh -c predict.sh"
    )

    use_dry_run = st.checkbox("Use Dry Run")
    check_airflow = st.checkbox("Check Airflow DAG Using REST API")

    submitted = st.button(
        "Serve Model ๐", disabled=not dag_id or not dag_schedule_interval or not docker_image or not docker_entrypoint
    )
    if submitted:
        req = CreateBatchRequest(
            docker_image=docker_image, schedule=dag_schedule_interval, entrypoint=docker_entrypoint, dag_id=dag_id
        )
        res = use_case.execute(req)
        st.success(f"DAG ์คํฌ๋ฆฝํธ ์์ฑ์ด ์๋ฃ๋์์ต๋๋ค.")
        st.download_button("Download DAG Script File", data=res.dag, file_name=f"somlier_offline_dag_{dag_id}.py")


else:
    dag_start_date = st.date_input("DAG Start Date").strftime("%Y-%m-%d")
    mlflow_model_ref = st.text_input(
        "MLflow Model Reference",
        placeholder="MLflow Model Registry์ ์กด์ฌํ๋ ๋ชจ๋ธ ์ ๋ณด๋ฅผ ์๋ ฅํ์ธ์.",
        help="e.g., boston-house-pricing/2",
    )
    dataset_ref = st.text_input(
        "Feature Dataset Table Reference (BigQuery)",
        placeholder="๋ชจ๋ธ์ ์๋ ฅ์ด ๋  BigQuery ํ์ด๋ธ ์ ๋ณด๋ฅผ ์๋ ฅํ์ธ์.",
        help="e.g., temp_serena.boston_house_pricing_feature_set",
    )
    dataset_load_column = st.text_input(
        "Column Name for Loading Dataset",
        placeholder="์ธํผ๋ฐ์ค ๋์์ ๊ธฐ์ค์ด ๋๋ ์ปฌ๋ผ ์ด๋ฆ์ ์๋ ฅํ์ธ์.",
        help="e.g., date",
    )
    dataset_load_by_kst = (
        st.radio("Column Timezone for Loading Dataset", ("KST(Asia/Seoul')", "UTC")) == "KST(Asia/Seoul')"
    )
    destination_table_ref = st.text_input(
        "Destination Table Reference (BigQuery)",
        placeholder="์ธํผ๋ฐ์ค ๊ฒฐ๊ณผ๊ฐ์ด ์ ์ฌ๋  BigQuery ํ์ด๋ธ ์ ๋ณด๋ฅผ ์๋ ฅํ์ธ์.",
        help="e.g., temp_serena.boston_house_pricing_result",
    )
    github_personal_access_token = st.text_input(
        "Github Personal Access Token",
        type="password",
        placeholder="Pull Request ์์ฑ์ ์ํ Personal Access Token ๊ฐ",
    )
    submitted = st.button(
        "Serve Model ๐",
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
        st.success(f"DAG ์์ฑ ๋ฐ PR ์์ฑ์ด ์๋ฃ๋์์ต๋๋ค.")
        st.success(res.msg)
