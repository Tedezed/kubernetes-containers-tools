#!/usr/bin/env python
import argparse
import sys, os
from proxy_server import ProxyServer
import store_credentials
import credentials_emailing

# Example:
# python mail_relay.py --remotehost localhost --remoteport 2505
# python mail_relay.py --certfile /tmp/server.crt --keyfile /tmp/server.key --remotehost localhost --remoteport 2505

pid = str(os.getpid())
pidfile = "/tmp/mailrelay.pid"

if os.path.isfile(pidfile):
    print "%s already exists, exiting" % pidfile
    sys.exit()

file(pidfile, 'w').write(pid)

def run(cmdargs):
    args = [
        (cmdargs.localhost, cmdargs.localport),
        (cmdargs.remotehost, cmdargs.remoteport)
    ]
    kwargs = {}

    if cmdargs.sslboth:
        kwargs['ssl'] = True
        if not cmdargs.certfile or not cmdargs.keyfile:
            print ('You need to specify a valid certificate file and a key file!')
            sys.exit(1)
        kwargs['certfile'] = cmdargs.certfile
        kwargs['keyfile'] = cmdargs.keyfile
    elif cmdargs.sslout:
        kwargs['ssl_out_only'] = True

    kwargs['debug'] = False

    if cmdargs.username and cmdargs.password:
        credentials = store_credentials.StoreCredentials()
        credentials.username = cmdargs.username
        credentials.password = cmdargs.password
        credentials.stored = True
    else:
        credentials = credentials_emailing.StoreCredentials()
        #credentials.username = config.username
        #credentials.password = config.password
        credentials.stored = True
    kwargs['credential_validator'] = credentials

    server = ProxyServer(*args, **kwargs)
    server.run()

parser = argparse.ArgumentParser(description='mail relay tool')

parser.add_argument(
    '--localhost',
    default='127.0.0.1',
    help='Local address to attach to for receiving mail.  Defaults to 127.0.0.1'
)

parser.add_argument(
    '--localport',
    default=1025,
    type=int,
    help='Local port to attach to for receiving mail.  Defaults to 1025'
)

parser.add_argument(
    '--remotehost',
    required=True,
    help='Address of the remote server for connection.'
)

parser.add_argument(
    '--remoteport',
    default=25,
    type=int,
    help='Port of the remote server for connection.  Defaults to 25'
)

parser.add_argument(
    '--quiet',
    action='store_true',
    help='Use this to turn off the message printing'
)

group = parser.add_mutually_exclusive_group()

group.add_argument(
    '--sslboth',
    action='store_true',
    help='Use this parameter if both the inbound and outbound connections should use SSL'
)

group.add_argument(
    '--sslout',
    action='store_true',
    help='Use this parameter if inbound connection is plain but the outbound connection uses SSL'
)

parser.add_argument(
    '--certfile',
    help='Certificate file to use for inbound SSL connections'
)

parser.add_argument(
    '--keyfile',
    help='Key file to use for inbound SSL connections'
)

parser.add_argument(
    '--username',
    help='Username for remote authentication'
)

parser.add_argument(
    '--password',
    help='Password for remote authentication'
)

args = parser.parse_args()

print('Starting ProxyServer')
print('local: %s:%s' % (args.localhost, args.localport))
print('remote: %s:%s' % (args.remotehost, args.remoteport))
print('sslboth: ', args.sslboth)
print('sslout: ', args.sslout)
print('')
run(args)
