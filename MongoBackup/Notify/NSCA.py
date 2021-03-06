import logging
import sys

from pynsca import NSCANotifier


class NotifyNSCA:
    def __init__(self, server, check_name, check_host, password=None):
        self.server     = server
        self.check_name = check_name
        self.check_host = check_host
        self.password   = password
        self.success    = 0
        self.warning    = 1
        self.critical   = 2
        self.notifier   = None

	split = self.server.split(":")
        self.server_name = split[0]
        self.server_port = 5667
        if len(split) == 2:
            self.server_port = int(split[1])

        self.mode_type  = ''
        self.encryption = 1
        if self.password:
            self.mode_type  = 'Secure '
            self.encryption = 16

        req_attrs = ['server', 'check_name', 'check_host']
        for attr in req_attrs:
            if not getattr(self, attr):
                raise Exception, 'NSCA module requires attribute: %s!' % attr, None

        try:
            self.notifier = NSCANotifier(
                monitoring_server=self.server_name,
                monitoring_port=self.server_port,
                encryption_mode=self.encryption,
                password=self.password
            )
        except Exception, e:
            logging.error('Error initiating NSCANotifier! Error: %s' % e)
            raise e

    def notify(self, ret_code, output):
        if self.notifier:
            logging.info("Sending %sNSCA report to check host/name '%s/%s' at NSCA host %s" % (
                self.mode_type,
                self.check_host,
                self.check_name,
                self.server
            ))
            # noinspection PyBroadException
            try:
                self.notifier.svc_result(self.check_host, self.check_name, ret_code, str(output))
            except Exception:
                logging.error('Failed to send %sNSCA report to host %s: %s' % (self.mode_type, self.server, sys.exc_info()[1]))

            logging.debug('Sent %sNSCA report to host %s' % (self.mode_type, self.server))
