import os
import platform
import sys
import signal
import time


class Daemon(object):
    """
    守护进程基类
    继承它然后实现run方法
    调用start开启守护进程
    调用stop停止守护进程
    """
    __pid_file = "/tmp/cyeap_daemon.pid"  # 默认PID文件位置

    def __init__(self, pid_file=None):
        if platform.system() == "Linux":
            if pid_file:
                self.__pid_file = pid_file
        else:
            raise OSError("The operating system does not support")  # 不支持其他操作系统

    def __get_pid(self):
        """
        从PID文件中读取进程ID
        :return:
        """
        try:
            with open(self.__pid_file) as f:  # 读取PID文件
                pid = int(f.read().strip())  # 去掉空格,并转换成int类型
        except Exception as ex:
            pid = None  # 打开PID文件失败,或读取错误
        return pid

    def __create_daemon(self):
        """
        创建一个守护进程
        :return:
        """
        # 从父进程fork一个子进程出来
        child_pid = os.fork()  # 这时候会就有两个进程在跑,一个父进程,一个子进程
        if child_pid:
            sys.exit(0)  # 退出父进程,子进程继续运行(子进程的child_pid=None所以不会执行退出)
        # 脱离控制终端,登录会话和进程组
        os.setsid()  # 让子进程成为新的会话组长和进程组长,与原会话彻底脱离
        os.chdir('/')  # 子进程默认继承父进程的工作目录，最好是变更到根目录，否则回影响文件系统的卸载
        os.umask(0)  # 子进程默认继承父进程的umask（文件权限掩码），重设为0（完全控制），以免影响程序读写文件
        # 现在,子进程已经成为无终端的会话组长。但它可以重新申请打开一个控制终端，session leader具备重新打开控制终端的能力
        # 如果子进程重新打开一个控制终端,那么这个控制终端的进程ID就会成为该子进程的父ID,背离了守护进程的意义
        # 所以 fork 第二个子进程,使之成为守护进程(不是必须,只是为了禁止守护进程打开新的控制终端)
        daemon_pid = os.fork()
        if daemon_pid:
            sys.exit(0)  # 结束第一子进程，第二子进程继续运行成为守护进程（第二子进程不是会话组长,不具备打开控制终端的能力）
        # ---------------------------输入输出重定向(可选) START---------------------------------- #
        # # 刷新缓冲区
        # sys.stdout.flush()
        # sys.stderr.flush()
        # # dup2函数原子化地关闭和复制文件描述符，重定向到/dev/nul，即丢弃所有输入输出
        # with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        #     os.dup2(read_null.fileno(), sys.stdin.fileno())
        #     os.dup2(write_null.fileno(), sys.stdout.fileno())
        #     os.dup2(write_null.fileno(), sys.stderr.fileno())
        # ---------------------------输入输出重定向(可选) END ---------------------------------- #
        # 将进程ID写入PID文件
        if self.__pid_file:
            with open(self.__pid_file, 'w+') as f:
                f.write(str(os.getpid()))

    def run(self):
        """
        子类必须实现此方法,即在守护进程中要做的thing
        :return:
        """
        raise NotImplementedError('Please define "a run method"')

    def start(self):
        """
        启动守护进程
        :return:
        """
        pid = self.__get_pid()
        if pid:  # pid 文件已经存在
            print("pid_file [%s] already exist.Daemon already running?\n" % self.__pid_file)
            sys.exit(1)
        else:
            self.__create_daemon()
            self.run()

    def stop(self):
        """
        停止守护进程
        :return:
        """
        pid = self.__get_pid()
        if pid:
            os.remove(self.__pid_file)  # 删除PID文件
            try:
                os.kill(pid, signal.SIGTERM)  # 杀掉进程
            except ProcessLookupError:
                print("No such process!")  # 找不到进程
        else:
            print("Not found pid_file [%s]\n" % self.__pid_file)  # 找不到pid_file

    def restart(self):
        """
        重新启动守护进程
        :return:
        """
        temp_pid = os.fork()  # 因为要自杀,自杀后,无法进行启动,所以临时fork一个进程用来启动守护进程
        if temp_pid:
            self.stop()  # 停止
            sys.exit(0)
        time.sleep(3)
        self.start()  # 启动