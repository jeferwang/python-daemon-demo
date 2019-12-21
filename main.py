#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import errno
import signal

SUPPORTED_OS = 'posix'
PID_FILE = '/var/run/test.pid'


def check_os():
    if os.name != SUPPORTED_OS:
        raise RuntimeError("仅支持Linux环境")


def get_action():
    if len(sys.argv) < 2:
        raise RuntimeError("Action List: start|stop")
    return sys.argv[1]


def write_pid(pid):
    with open(PID_FILE, 'w') as f:
        f.write(str(pid))


def get_pid():
    with open(PID_FILE, 'r') as f:
        return int(f.read())


def clear_pid():
    os.unlink(PID_FILE)


def kill_process():
    pid = get_pid()
    os.kill(pid, signal.SIGINT)
    clear_pid()


def start():
    pid = os.fork()

    assert pid != -1

    if pid > 0:
        # pid不为0的是父进程
        write_pid(pid)
        sys.exit(0)  # 父进程退出之后，fork出来的子进程会自动挂载pid为1的进程下

    # ppid = os.getppid()
    # pid = os.getpid()
    # print("ppid", ppid)
    # print("pid", pid)

    # daemon do sth
    sys.stdin.close()
    sys.stdout.close()
    sys.stderr.close()
    while True:
        pass


def main():
    check_os()

    action = get_action()

    if action == 'start':
        start()
    elif action == 'stop':
        kill_process()


if __name__ == "__main__":
    main()
