import subprocess
import logging
import shlex

LOG = logging.getLogger("OIIInspector")


def run_cmd(cmd, err_msg=None, tolerate_err=False):
    """
    Run a command locally.
    Args:
        cmd (str):
            Shell command to be executed.
        err_msg (str):
            Error message written when the command fails.
        tolerate_err (bool):
            Whether to tolerate a failed command.

    Returns (str, str):
        Tuple of stdout and stderr generated by the command.
    """
    err_msg = err_msg or "An error has occurred when executing a command."
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode != 0 and not tolerate_err:
        LOG.error("Command {0} failed with {1}".format(cmd, err))
        raise RuntimeError("API call was not successful")
    return out.decode('utf-8')
