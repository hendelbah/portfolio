class Styles:
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'


class RacingReportException(Exception):
    """
    Exception class for local exceptions
    """


class IncompleteDataError(RacingReportException):
    """
    Raise this when some data files is missing
    """


class SearchError(RacingReportException):
    """
    Raise this when search fails
    """


__all__ = ['Styles', 'SearchError', 'RacingReportException', 'IncompleteDataError']
