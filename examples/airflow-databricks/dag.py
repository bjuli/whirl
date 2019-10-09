from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.databricks_operator import DatabricksRunNowOperator

args = {
    'owner': 'whirl',
    'start_date': datetime(2019, 1, 1),
    'end_date': datetime(2019, 1, 31),
    'depends_on_past': True,
}
with DAG(
    dag_id='databricks_airflow',
    default_args=args,
    schedule_interval='0 8 * * *',
    catchup=True,
    max_active_runs=1,
) as dag:
    runnow2 = DatabricksRunNowOperator(
        job_id=2,
        task_id='databricks-airflow-task-id',
        databricks_conn_id="databricks_default",
        execution_timeout=timedelta(minutes=60),
    )
    runnow25 = DatabricksRunNowOperator(
        job_id=25,
        task_id='databricks-airflow-task-id',
        databricks_conn_id="databricks_default",
        execution_timeout=timedelta(minutes=60),
    )


runnow2 >> runnow25
