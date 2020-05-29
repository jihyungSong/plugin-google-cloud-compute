# -*- coding: utf-8 -*-

from spaceone.core import error


class ERROR_REPOSITORY_BACKEND(error.ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Repository backend has problem. ({host})'
