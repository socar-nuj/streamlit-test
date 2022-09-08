import streamlit as st
from frontend.controller import online_container
from somlier.application.use_cases.online.search import SearchRequest

use_case = online_container.container.search()

st.markdown("## Search Model By Metric 😎")
st.markdown("""---""")

# TODO(serena): 사용성을 개선하기 위해 dropdown으로 변경할 수 있다. -> usecase쪽 변경이 필요함
project_name = st.text_input("MLflow Experiment Name", placeholder="실험이 기록된 MLflow experiment 이름을 입력하세요.")
metric = st.text_input("Metric", placeholder="정렬 및 검색에 사용할 metric 이름을 입력하세요.")
ascending = st.radio("Ascending / Descending", ("Ascending", "Descending"))

submitted = st.button("Search 🔖", disabled=not project_name or not metric)

if submitted:
    if ascending == "Ascending":
        req = SearchRequest(project_name=project_name, metric_by=metric, ascending=True)
    else:
        req = SearchRequest(project_name=project_name, metric_by=metric, ascending=False)
    res = use_case.execute(req)
    st.success(f"결과 Run id: {res.run_id} / 결과 Metric 값: {res.metric_value}")
