from datetime import datetime, timedelta

from airflow.models import DAG
from custom_operators.databricks_xcom_operator import (
    DatabricksJobGetIdOperator,
    DatabricksJobFromXCOMRunNowOperator
)

args = {
    'owner': 'whirl',
    'start_date': datetime(2019, 1, 1),
    'end_date': datetime(2019, 1, 31),
    'depends_on_past': True,
}
with DAG(
    dag_id='databicks-backfill',
    default_args=args,
    schedule_interval='0 8 * * *',
    catchup=True,
    max_active_runs=1,
) as dag:
    getid = DatabricksJobGetIdOperator(
        task_id='databricks-get-job-id',
        job_name='name-of-existing-job',
        databricks_conn_id="databricks_default",
        execution_timeout=timedelta(minutes=5),

    )
    runnow = DatabricksJobFromXCOMRunNowOperator(
        task_id='databricks-run-job-id',
        databricks_conn_id="databricks_default",
        xcom_push_task_id='databricks-get-job-id',
        execution_timeout=timedelta(minutes=60),
    )

getid >> runnow
