import platform
import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
import subprocess
import time


def collect_webapp(pid):
    """
    要定时执行的函数
    :param args: 参数
    :return: None
    """
    try:
        webapps = subprocess.check_output('ls /local/webapp/', shell=True)
        fout = open('/tmp/demone.log', 'w')
        fout.write(webapps.decode(encoding='utf-8'))
        fout.close()
    except Exception as ex:
        print(ex)
        os.kill(pid)


def createDaemon():
    # fork进程
    try:
        if os.fork() > 0:
            sys.exit(0)
    except OSError as error:
        print('fork #1 failed: %d (%s)' % (error.errno, error.strerror))
        sys.exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            print('Daemon PID %d' % pid)
            sys.exit(0)
    except OSError as error:
        print('fork #2 failed: %d (%s)' % (error.errno, error.strerror))
        sys.exit(1)
    # 重定向标准IO
    sys.stdout.flush()
    sys.stderr.flush()
    # 在子进程中执行代码
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_webapp, trigger='interval', seconds=3)
    scheduler.start()
    while True:
        time.sleep(3)

if __name__ == '__main__':
    if platform.system() == "Linux":
        createDaemon()
    else:
        sys.exit(0)
