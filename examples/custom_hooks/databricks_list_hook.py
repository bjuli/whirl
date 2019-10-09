from airflow.contrib.hooks.databricks_hook import DatabricksHook

LIST_ENDPOINT = ('GET', 'api/2.0/jobs/list')


class DatabricksListHook(DatabricksHook):
    """
    Interact with Databricks.
    """
    def __init__(
        self,
        databricks_conn_id='databricks_default',
        timeout_seconds=180,
        retry_limit=3,
        retry_delay=1.0):
        """
        :param databricks_conn_id: The name of the databricks connection to use.
        :type databricks_conn_id: str
        :param timeout_seconds: The amount of time in seconds the requests library
            will wait before timing-out.
        :type timeout_seconds: int
        :param retry_limit: The number of times to retry the connection in case of
            service outages.
        :type retry_limit: int
        :param retry_delay: The number of seconds to wait between retries (it
            might be a floating point number).
        :type retry_delay: float
        """
        super(DatabricksListHook, self).__init__(
            databricks_conn_id=databricks_conn_id,
            timeout_seconds=timeout_seconds,
            retry_limit=retry_limit,
            retry_delay=retry_delay
        )

    def list(self):
        """
        Utility function to call the ``api/2.0/jobs/list`` endpoint.
        :return: the list of jobs as json
        :rtype: dict
        """
        response = super(DatabricksListHook, self)._do_api_call(LIST_ENDPOINT, {})
        return response
