#!venv/bin/python

import os
from multiprocessing import cpu_count


def max_workers():
    return cpu_count() * 2 + 1


def run_with_gunicorn():
    cmd = "gunicorn -w {workers} -b {host}:{port} fnote.app:app --pid=gunicorn_manual.pid".format(
        workers=max_workers(), host='0.0.0.0', port=9000
    )
    print("#", cmd)
    os.system(cmd)


if __name__ == "__main__":
    run_with_gunicorn()
