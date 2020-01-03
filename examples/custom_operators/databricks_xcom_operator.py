from airflow.models import BaseOperator
from airflow.contrib.operators.databricks_operator import DatabricksRunNowOperator

from airflow.utils.decorators import apply_defaults
from examples.custom_hooks.databricks_list_hook import DatabricksListHook
import logging

logFormat = "[%(levelname)-5.5s]%(message)s"
logging.basicConfig(level=logging.INFO, format=logFormat)
log = logging.getLogger()


class DatabricksJobFromXCOMRunNowOperator(DatabricksRunNowOperator):
    """
    Runs an existing Spark job run to Databricks using the
    `api/2.0/jobs/run-now
    <https://docs.databricks.com/api/latest/jobs.html#run-now>`_
    API endpoint.
    There are two ways to instantiate this operator.
    In the first way, you can take the JSON payload that you typically use
    to call the ``api/2.0/jobs/run-now`` endpoint and pass it directly
    to our ``DatabricksJobFromXCOMRunNowOperator`` through the ``json`` parameter.
    For example ::
        json = {
          "notebook_params": {
            "dry-run": "true",
            "oldest-time-to-consider": "1457570074236"
          }
        }
        notebook_run = DatabricksJobFromXCOMRunNowOperator(task_id='notebook_run', json=json)
    Another way to accomplish the same thing is to use the named parameters
    of the ``DatabricksJobFromXCOMRunNowOperator`` directly. Note that there is exactly
    one named parameter for each top level parameter in the ``run-now``
    endpoint. In this method, your code would look like this: ::
        notebook_params = {
            "dry-run": "true",
            "oldest-time-to-consider": "1457570074236"
        }
        python_params = ["douglas adams", "42"]
        spark_submit_params = ["--class", "org.apache.spark.examples.SparkPi"]
        notebook_run = DatabricksRunNowOperator(
            job_id=job_id,
            notebook_params=notebook_params,
            python_params=python_params,
            spark_submit_params=spark_submit_params
        )
    In the case where both the json parameter **AND** the named parameters
    are provided, they will be merged together. If there are conflicts during the merge,
    the named parameters will take precedence and override the top level ``json`` keys.
    Currently the named parameters that ``DatabricksJobFromXCOMRunNowOperator`` supports are
        - ``json``
        - ``notebook_params``
        - ``python_params``
        - ``spark_submit_params``
    :param json: A JSON object containing API parameters which will be passed
        directly to the ``api/2.0/jobs/run-now`` endpoint. The other named parameters
        (i.e. ``notebook_params``, ``spark_submit_params``..) to this operator will
        be merged with this json dictionary if they are provided.
        If there are conflicts during the merge, the named parameters will
        take precedence and override the top level json keys. (templated)
        .. seealso::
            For more information about templating see :ref:`jinja-templating`.
            https://docs.databricks.com/api/latest/jobs.html#run-now
    :type json: dict
    :param notebook_params: A dict from keys to values for jobs with notebook task,
        e.g. "notebook_params": {"name": "john doe", "age":  "35"}.
        The map is passed to the notebook and will be accessible through the
        dbutils.widgets.get function. See Widgets for more information.
        If not specified upon run-now, the triggered run will use the
        job’s base parameters. notebook_params cannot be
        specified in conjunction with jar_params. The json representation
        of this field (i.e. {"notebook_params":{"name":"john doe","age":"35"}})
        cannot exceed 10,000 bytes.
        This field will be templated.
        .. seealso::
            https://docs.databricks.com/user-guide/notebooks/widgets.html
    :type notebook_params: dict
    :param python_params: A list of parameters for jobs with python tasks,
        e.g. "python_params": ["john doe", "35"].
        The parameters will be passed to python file as command line parameters.
        If specified upon run-now, it would overwrite the parameters specified in
        job setting.
        The json representation of this field (i.e. {"python_params":["john doe","35"]})
        cannot exceed 10,000 bytes.
        This field will be templated.
        .. seealso::
            https://docs.databricks.com/api/latest/jobs.html#run-now
    :type python_params: list[str]
    :param spark_submit_params: A list of parameters for jobs with spark submit task,
        e.g. "spark_submit_params": ["--class", "org.apache.spark.examples.SparkPi"].
        The parameters will be passed to spark-submit script as command line parameters.
        If specified upon run-now, it would overwrite the parameters specified
        in job setting.
        The json representation of this field cannot exceed 10,000 bytes.
        This field will be templated.
        .. seealso::
            https://docs.databricks.com/api/latest/jobs.html#run-now
    :type spark_submit_params: list[str]
    :param timeout_seconds: The timeout for this run. By default a value of 0 is used
        which means to have no timeout.
        This field will be templated.
    :type timeout_seconds: int32
    :param databricks_conn_id: The name of the Airflow connection to use.
        By default and in the common case this will be ``databricks_default``. To use
        token based authentication, provide the key ``token`` in the extra field for the
        connection.
    :type databricks_conn_id: str
    :param polling_period_seconds: Controls the rate which we poll for the result of
        this run. By default the operator will poll every 30 seconds.
    :type polling_period_seconds: int
    :param databricks_retry_limit: Amount of times retry if the Databricks backend is
        unreachable. Its value must be greater than or equal to 1.
    :type databricks_retry_limit: int
    :param do_xcom_push: Whether we should push run_id and run_page_url to xcom.
    :type do_xcom_push: bool
    :param xcom_push_task_id: Task id that pushed the job id for this operator to use.
    :type xcom_push_task_id: str
    """
    # Used in airflow.models.BaseOperator
    template_fields = ('json',)
    # Databricks brand color (blue) under white text
    ui_color = '#1CB1C2'
    ui_fgcolor = '#fff'

    @apply_defaults
    def __init__(
        self,
        json=None,
        notebook_params=None,
        python_params=None,
        spark_submit_params=None,
        databricks_conn_id='databricks_default',
        polling_period_seconds=30,
        databricks_retry_limit=3,
        databricks_retry_delay=1,
        do_xcom_push=False,
        xcom_push_task_id='databricks_run_now_id_getter',
        **kwargs):

        """
        Creates a new ``DatabricksRunNowOperator``.
        """
        super(DatabricksJobFromXCOMRunNowOperator, self).__init__(
            job_id=None,
            json=json,
            notebook_params=notebook_params,
            python_params=python_params,
            spark_submit_params=spark_submit_params,
            databricks_conn_id=databricks_conn_id,
            polling_period_seconds=polling_period_seconds,
            databricks_retry_limit=databricks_retry_limit,
            databricks_retry_delay=databricks_retry_delay,
            do_xcom_push=do_xcom_push,
            **kwargs
        )
        self.xcom_push_task_id = xcom_push_task_id

    def _get_job_id_from_xcom(self, context):
        job_id = context['task_instance'].xcom_pull(task_ids=self.xcom_push_task_id, key='job_id')
        return job_id

    def execute(self, context):
        job_id = self._get_job_id_from_xcom(context)
        if job_id is not None:
            self.json['job_id'] = job_id
        super(DatabricksJobFromXCOMRunNowOperator, self).execute(context)


class DatabricksJobGetIdOperator(BaseOperator):
    """
    Gets all job info from Databricks using the
    `api/2.0/jobs/list
    <https://docs.databricks.com/api/latest/jobs.html#list>`_
    API endpoint.
    It will filter on the provided job name and push the job_id to xcom if needed.

    :param job_name: the job_name of the existing Databricks job.
        This field will be templated.
        .. seealso::
            https://docs.databricks.com/api/latest/jobs.html#list
    :type job_name: str
    :param databricks_conn_id: The name of the Airflow connection to use.
        By default and in the common case this will be ``databricks_default``. To use
        token based authentication, provide the key ``token`` in the extra field for the
        connection.
    :type databricks_conn_id: str
    :param polling_period_seconds: Controls the rate which we poll for the result of
        this run. By default the operator will poll every 30 seconds.
    :type polling_period_seconds: int
    :param databricks_retry_limit: Amount of times retry if the Databricks backend is
        unreachable. Its value must be greater than or equal to 1.
    :type databricks_retry_limit: int

    :param do_xcom_push: Whether we should push job_id to xcom.
    :type do_xcom_push: bool
    """
    # Used in airflow.models.BaseOperator
    template_fields = ('job_name',)
    # Databricks brand color (blue) under white text
    ui_color = '#1CB1C2'
    ui_fgcolor = '#fff'

    @apply_defaults
    def __init__(
        self,
        job_name,
        databricks_conn_id='databricks_default',
        databricks_retry_limit=3,
        databricks_retry_delay=1,
        do_xcom_push=True,
        **kwargs):

        """
        Creates a new ``DatabricksJobGetIdOperator``.
        """
        super(DatabricksJobGetIdOperator, self).__init__(**kwargs)
        self.job_name = job_name
        self.databricks_conn_id = databricks_conn_id
        self.databricks_retry_limit = databricks_retry_limit
        self.databricks_retry_delay = databricks_retry_delay
        self.do_xcom_push = do_xcom_push

    def get_hook(self):
        return DatabricksListHook(
            self.databricks_conn_id,
            retry_limit=self.databricks_retry_limit,
            retry_delay=self.databricks_retry_delay)

    def find_current_job_id(self, joblist: dict) -> int:
        jobs = joblist['jobs']
        result = list(filter(lambda job: job['settings']['name'].startswith(self.job_name), jobs))
        if len(result) > 0:
            return max([result[i].get('job_id', -1) for i in range(len(result))])

    def execute(self, context):
        job_id = -1
        hook = self.get_hook()
        joblist = hook.list()
        log.info(joblist)
        if 'jobs' in joblist:
            job_id = self.find_current_job_id(joblist)
            log.info("The current job-id is {}".format(job_id))
        if self.do_xcom_push:
            context['task_instance'].xcom_push(key='job_id', value=job_id)
        return job_id
