"""
Enable HTTP requests/responses logging.

Usage:

>>> import logging
>>> from spqr.kieran.httplog import logRoundtrip, HttpFormatter

>>> formatter = HttpFormatter("{asctime}|{levelname}|{threadName}|{message}", style="{")
>>> handler = logging.StreamHandler()
>>> handler.setFormatter(formatter)
>>> logging.basicConfig(level=loglevel, handlers=[handler])

>>> session = requests.Session()
>>> session.hooks['response'].append(logRoundtrip)

"""

import logging
import textwrap

_lg = logging.getLogger('httplogger')


def logRoundtrip(response, *args, **kwargs):
    """ Requests hook to log HTTP request and response. """
    extra = {'req': response.request, 'res': response}
    _lg.debug('HTTP roundtrip', extra=extra)


class HttpFormatter(logging.Formatter):

    def _formatHeaders(self, d):
        return '\n'.join(f'{k}: {v}' for k, v in d.items())

    def formatMessage(self, record):
        result = super().formatMessage(record)
        if record.name == 'httplogger':
            result += textwrap.dedent('''
                ---------------- request ----------------
                {req.method} {req.url}
                {reqhdrs}

                {req.body}
                ---------------- response ----------------
                {res.status_code} {res.reason} {res.url}
                {reshdrs}

                {res.text}
            ''').format(
                req=record.req,
                res=record.res,
                reqhdrs=self._formatHeaders(record.req.headers),
                reshdrs=self._formatHeaders(record.res.headers),
            )

        return result
