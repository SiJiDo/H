import time
import signal
from subprocess import Popen

class SubProcessSrc(object):
    """Running the process in a separate thread
       and outputting the stdout and stderr simultaneously.
       result dict with status and proc. status = 1 means process not completed.
       status = 0 means process completed successfully.
    """
    def __init__(self, cmd, cwd, shell=False, timeout=604800):
        self.cmd = cmd
        self.timeout = timeout
        self.proc = None
        self.shell = shell
        self.revoked = False
        self.cwd = cwd

    def run(self):
        signal.signal(signal.SIGTERM, self.sigterm_hander)
        self.proc = Popen(self.cmd, shell=self.shell, cwd=self.cwd)
        for i in self.proc:
            print(i)
        is_timeout = True
        for i in range(self.timeout):
            if self.proc.poll() is not None:
                is_timeout = False
                break
            time.sleep(1)

        result = {'proc': self.proc}

        if self.revoked:
            result['status'] = -1
        elif is_timeout: # Process not completed
            result['status'] = 1
        else:  # Process completed successfully.
            result['status'] = 0

        return result

    def sigterm_hander(self, signum, frame):
        self.proc.terminate()
        self.proc.wait()
        self.revoked = True

