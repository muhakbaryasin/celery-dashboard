import http.cookiejar
import urllib.request
import urllib.parse
import ssl
from time import sleep
import logging
import gzip


class Scraper(object):
    def __init__(self, verify=True):
        """
        kwarg
        **urllibArg = {url, data, headers={}, origin_req_host=None, unverifiable=False, method=None}
        urllib.request.Request()
        """
        self.cookiejar = http.cookiejar.CookieJar()
        context = None

        if not verify:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        hh = urllib.request.HTTPHandler(debuglevel=0)
        hsh = urllib.request.HTTPSHandler(debuglevel=0, context=context)
        cp = urllib.request.HTTPCookieProcessor(self.cookiejar)

        self.opener = urllib.request.build_opener(hh, hsh, cp)
        self.opener.addheaders = \
            [('User-agent',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/48.0.2564.103 Safari/537.36')]

    def request_data(self, referer=None, x_requested_with=None, content_type=None, timeout=60, attempt=0, **urllib_arg):
        try:
            # This is the Request
            is_json = False

            if urllib_arg['method'] == 'POST_JSON':
                is_json = True
                urllib_arg['method'] = 'POST'

            req = urllib.request.Request(**urllib_arg)

            for each_ in self.cookiejar:
                req.add_header('Cookie', '{}={}'.format(each_.name, each_.value))

            if referer is not None:
                req.add_header('Referer', referer)
            if x_requested_with is not None:
                req.add_header('X-Requested-With', x_requested_with)
            if content_type is not None:
                req.add_header('Content-Type', content_type)
            if is_json:
                req.add_header('Content-Type', 'application/json')

            site = self.opener.open(req, timeout=timeout)

            if site.info().get('Content-Encoding') == 'gzip':
                response_data = gzip.decompress(site.read())
            else:
                response_data = site.read()

        except Exception as e:
            if attempt < 2:
                sleep(3)
                cookie = self.cookiejar
                self.__init__()
                self.cookiejar = cookie
                self.request_data(referer=referer, x_requested_with=x_requested_with, content_type=None,
                                  timeout=timeout + 10, attempt=attempt + 1, **urllib_arg)
            logging.error("Unable to request {}. Error {}".format(urllib_arg['url'], str(e)))
            return None

        return response_data

    def get_session(self):
        return self.opener

    def set_session(self, opener):
        self.opener = opener
