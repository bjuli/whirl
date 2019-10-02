from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.databricks_operator import DatabricksRunNowOperator

args = {
    'owner': 'databricks',
    'start_date': datetime(2019, 1, 1),
    'end_date': datetime(2019, 1, 31),
    'depends_on_past': True,
}
with DAG(
    dag_id='databricks-airflow',
    default_args=args,
    schedule_interval='0 8 * * *',
    catchup=True,
    max_active_runs=1,
) as dag:
    runnow = DatabricksRunNowOperator(
        job_id=25,
        task_id='databricks-airflow-task-id',
        databricks_conn_id="databricks_default",
        execution_timeout=timedelta(minutes=60),
    )

    dumb = DummyOperator(
        task_id="this-is-a-Dummy"
    )

runnow >> dumb
