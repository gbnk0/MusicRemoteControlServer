from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urlparse
import MrcLogger
from MrcCommander import MrcCommander

class MrcHTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        MrcLogger.info('[GET] START')
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        MrcLogger.info('[GET] '+message)
        return

    def do_POST(self):
        mc=MrcCommander()

        wholerfile=''
        for inputline in self.rfile:
            wholerfile+=inputline
            inputline = inputline.rstrip()
            mc.analyseReceivedLine(inputline)
            if mc.cmd:
                MrcLogger.info('QUERY: '+inputline)
                break
            if inputline=='':
                MrcLogger.error('QUERY: INVALID! No line in HTTPHandler\'s rfile could pass analysis!')
                MrcLogger.error(wholerfile)
                break

        if mc.cmd:
            mc.process()

        reply=mc.res
        if reply=='':
            reply='{"error":"empty reply"}'
        MrcLogger.info('REPLY: '+reply)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(reply)
        return

    def gatherInfo(self):
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        return message


class MrcThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class MrcHTTPServerThread(threading.Thread):

    def __init__(self, portnum):
        threading.Thread.__init__(self)
        self.portnum=portnum
        self.server=0

    def run(self):
        self.server = MrcThreadedHTTPServer(('', self.portnum), MrcHTTPHandler)
        sa=self.server.socket.getsockname()
        print ' ... HTTP server launched on '+str(sa[0])+' port '+str(sa[1])+' ...'
        MrcLogger.info(' ... HTTP server launched on '+str(sa[0])+' port '+str(sa[1])+' ...')
        self.server.serve_forever()
        print ' ... HTTP server stopped ...'
        MrcLogger.info(' ... HTTP server stopped ...')