class RequestsError(Exception):
    pass


def report_error(response):
    """
    Report an error from a REST request.

    response
        A response object corresponding to an API request.

        The caller will be responsible for checking the
        status code for an error.
    """

    url = response.url

    msg = (f'requests_error: {response.content}\nurl: {url} ')
    raise RequestsError(msg)
