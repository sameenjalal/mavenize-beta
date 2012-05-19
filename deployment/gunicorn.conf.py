import os

def num_cpus():
    """
    Returns the total amount of CPU's on the system.
    """
    if not hasattr(os, 'sysconf'):
        raise RunTimeError('No sysconf detected.')
    return os.sysconf('SC_NPROCESSORS_ONLN')

bind = '127.0.0.1:8000'
workers = num_cpus() * 2 + 1
