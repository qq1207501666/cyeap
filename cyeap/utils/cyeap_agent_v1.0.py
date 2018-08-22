import os
import sys
import signal
import platform
import json
import socket
import socketserver
import subprocess
import time


def get_ipv4():
    """
    获取本地IPv4地址
    :return:
    """
    # 注意外围使用双引号而非单引号,并且假设默认是第一个网卡,特殊环境请适当修改代码
    ipv4 = subprocess.check_output(
        "ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1", shell=True)
    ipv4 = ipv4.decode().replace("\n", "")  # 去掉换行符
    return ipv4


def send_data(host, port, data):
    """
    发送数据
    :param host:
    :param port:
    :param data:
    :return:
    """
    with socket.socket() as sk_client:
        sk_client.connect((host, port))
        sk_client.send(bytes(json.dumps(data), 'utf8'))
        response = sk_client.recv(1024)
        print(str(response, "utf-8"))


def decode(byte_str):
    """
    将字节对象进行解码
    将依次尝试使用encoding_list中的字符集进行解码,直至解码正确或尝试完所有字符集,进行返回
    :param byte_str: 字节对象
    :return: 解码后的字符串对象
    """
    encoding_list = ['UTF-8', 'GBK', ]
    for encoding in encoding_list:
        try:
            return byte_str.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("未知的字符集编码")


def svn_up(svn_path, r=None):
    """
    svn 更新指定目录
    :param svn_path: svn 路径
    :param r: 版本号,默认更新至最新版本
    :return: svn 更新结果
    """
    if r:
        result = subprocess.check_output(["svn", "up", "-r", str(r), svn_path])
    else:
        result = subprocess.check_output(["svn", "up", svn_path])
    return result


def get_tomcat_pid(tomcat_path):
    """
    获取Tomcat PID
    :param tomcat_path: tomcat目录
    :return: 进程ID号
    """
    assert os.path.isdir(tomcat_path), "tomcat_path must be a directory!"
    if tomcat_path[-1] == "/":
        tomcat_path = tomcat_path[:-1]  # 如果参数末尾以/结束,会导致搜索不到进程,进行截取处理
    assert os.path.exists("%s/bin/startup.sh" % tomcat_path), "Can't find startup.sh!"
    find_pid_cmd = "ps -ef | grep -v grep | grep '%s -Djava' | awk '{print $2}'" % tomcat_path  # 查找进程ID
    pid = subprocess.check_output(find_pid_cmd, shell=True)
    pid = pid.decode().replace("\n", "")  # 去掉换行符
    return pid


def restart_tomcat(tomcat_path, stop=False):
    """
    重启Tomcat
    :param tomcat_path: Tomcat 路径
    :param stop: 如果设置该参数为True,停止Tomcat后,将不再进行启动,强烈建议使用stop_tomcat()进行停止操作
    :return:
    """
    pid = get_tomcat_pid(tomcat_path)  # 获取Tomcat PID
    if pid:
        subprocess.call(["kill", "-9", pid])
        if stop:
            return pid
        time.sleep(1)
        subprocess.call(["%s/bin/startup.sh" % tomcat_path])
    else:
        subprocess.call(["%s/bin/startup.sh" % tomcat_path])


def stop_tomcat(tomcat_path):
    """
    停止Tomcat
    :param tomcat_path: Tomcat 路径
    :return: 被终止的Tomcat进程的PID
    """
    return restart_tomcat(tomcat_path, stop=True)


def upgrade_webapp(webapp_path, tomcat_path, revision=None):
    """
    主要功能1: 项目升级
    :param webapp_path: 项目部署路径
    :param tomcat_path: TomcatServer部署路径
    :param revision: 更新至项目版本号 revision 默认None为最新版本
    :return: 更新的内容
    """
    output = svn_up(webapp_path, r=revision)  # 更新项目
    if output:
        restart_tomcat(tomcat_path)  # 重启Tomcat
    return output


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


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    处理请求的socket server
    继承的BaseRequestHandler类,重写handle()方法用来处理请求
    """

    def handle(self):
        try:
            result = self.request.recv(1024)
            data = str(result, 'utf-8')
            result = json.loads(data)
            if isinstance(result, dict):
                cmd = result.get("cmd")  # 指令
                args = result.get("args")  # 参数集
                # 支持命令1: 项目升级
                if cmd == "upgrade":
                    output = upgrade_webapp(args["webapp_path"], args["tomcat_path"], revision=args["revision"])
                    self.request.sendall(output)  # 将更新结果返回
                # 支持命令2: Tomcat重启
                elif cmd == "restart_tomcat":  # 启动|停止|重启 Tomcat
                    if args["opt"] == "start" or args["opt"] == "restart":
                        restart_tomcat(args["tomcat_path"])  # 启动 与 重启
                        self.request.sendall(bytes("START OK", "utf-8"))
                    elif args["opt"] == "stop":
                        restart_tomcat(args["tomcat_path"], stop=True)  # 停止
                        self.request.sendall(bytes("STOP OK", "utf-8"))
                    else:
                        self.request.sendall(bytes("Incorrect args", "utf-8"))  # 错误的参数指令
                # 支持命令3: Tomcat状态检测
                elif cmd == "check_tomcat":
                    tomcat_path = args["tomcat_path"]
                    pid = get_tomcat_pid(tomcat_path)
                    if pid:
                        self.request.sendall(bytes("True", "utf-8"))  # 不支持的命令
                    else:
                        self.request.sendall(bytes("False", "utf-8"))  # 不支持的命令
                else:
                    self.request.sendall(bytes("Unsupported command", "utf-8"))  # 不支持的命令
            else:
                self.request.sendall(bytes("Incorrect data format", "utf-8"))  # 错误的数据格式
        except ConnectionResetError as error:
            print('ConnectionResetError: 客户端断开了连接 %s' % error)


class CyeapDaemon(Daemon):
    def run(self):
        """
        实现父类run方法,守护进程中运行socket server
        :return:
        """
        # 下方代码为获取当前主机IPV4 和IPV6的所有IP地址(所有系统均通用)
        host = get_ipv4()
        port = 6666  # 端口
        server = socketserver.ThreadingTCPServer((host, port), ThreadedTCPRequestHandler)
        print(host, port)
        server.serve_forever()  # 开启服务


# 运行socket服务
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cyeap_agent_v1.0.py [start | stop | restart]")
        sys.exit(0)
    daemon = CyeapDaemon()
    if sys.argv[1] == "start":
        print("[\033[0;32m%s\033[0m]" % "May the blessings of God be with you!")
        daemon.start()
    elif sys.argv[1] == "restart":
        daemon.restart()
    elif sys.argv[1] == "stop":
        print("[\033[0;32m%s\033[0m]" % "See you around!")
        daemon.stop()
    else:
        print("[\033[0;43m%s\033[0m]" % "Nothing to do!")
