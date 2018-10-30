# -*- encoding: utf-8 -*-

import re
from datetime import datetime
from collections import Counter


def parse(ignore_files=False, ignore_urls=[], start_at=None, stop_at=None,
          request_type=None, ignore_www=False, slow_queries=False):
    reg = '{date} "{request} {url} \S+" \d+ {p_time}'
    date = '\[(?P<datetime>\d+/\w+/\d+ \d+:\d+:\d+)\]'
    request = '\w+' if request_type is None else '(?:{})'.format("|".join(request_type))
    url_to_file = r'\w+://{}(?P<url>[\w.]+[^ \t\n\r\f\v]*)'
    url = r'\w+://{}(?P<url>[\w.]+[^ \t\n\r\f\v.]*)'
    if not ignore_files:
        url = url_to_file
    url = url.format("(?:www\.)?" if ignore_www else "")
    p_time = '(?P<p_time>\d+)' if slow_queries else '\d+'
    fields = {'date': date, 'request': request, 'url': url, 'p_time': p_time}
    reg = reg.format(**fields)
    reg = re.compile(reg)
    ignore_urls_set = set(ignore_urls)
    out_counter = Counter()
    if slow_queries:
        p_time = Counter()
    if start_at:
        start_at = datetime.strptime(start_at, '%d/%b/%Y %H:%M:%S')
    if stop_at:
        stop_at = datetime.strptime(stop_at, '%d/%b/%Y %H:%M:%S')
    with open('log.log') as f:
        for line in open('log.log'):
            match = reg.match(line)
            if match:
                match = match.groupdict()
                if start_at or stop_at:
                    log_datetime = datetime.strptime(match['datetime'], '%d/%b/%Y %H:%M:%S')
                if start_at:
                    if log_datetime < start_at:
                        continue
                if stop_at:
                    if log_datetime > stop_at:
                        break
                if ignore_urls:
                    if match['url'] in ignore_urls_set:
                        continue
                if slow_queries:
                    p_time[match['url']] += int(match['p_time'])
                out_counter[match['url']] += 1
        if slow_queries:
            for i in out_counter:
                out_counter[i] = p_time[i] // out_counter[i]
    out = [num[1] for num in out_counter.most_common(5)]
    return out


if __name__ == '__main__':
    parse()