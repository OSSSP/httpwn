import random

from logger import *

class RqGen:
    # most popular UAs accoring to http://www.browser-info.net/useragents
    USER_AGENTS = ['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.7.01001)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.5.01003)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8',
        'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705)',
        'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.02',
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1',
        'Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.0) Opera 7.02 Bork-edition [en]']

    def __init__(self, method, host, path, spoofUA, bodylen):
        self.CRLF = '\r\n'
        self.spoofUA = spoofUA
        self.bodylen = bodylen
        self.HTTP_REQUEST = [
            '{METHOD} {PATH} HTTP/1.1'.format(METHOD=method, PATH=path),
            'Host: {HOST}'.format(HOST=host),
            'User-Agent: {UA}',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: en-US;q=0.5,en;q=0.5',
            'Accept-Encoding: gzip, deflate',
            'Connection: close',
        ]

    def get_rand_UA(self):
        return RqGen.USER_AGENTS[random.randint(0, len(RqGen.USER_AGENTS) - 1)] if self.spoofUA else RqGen.USER_AGENTS[0]

    def gen_body(self):
        return "X" * self.bodylen

    def payload(self):
        body = self.gen_body()

        http_string = ''
        for rqline in self.HTTP_REQUEST:
            http_string += rqline + self.CRLF

        if self.bodylen:
            http_string += 'Content-Length: {BODYLEN}'.format(BODYLEN=len(body.encode())) + self.CRLF

        http_string = http_string.format(UA=self.get_rand_UA()) + self.CRLF

        if self.bodylen:
            http_string = http_string + body

        Logger.debug('\n' + http_string)
        return http_string
