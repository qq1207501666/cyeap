import redis
# Create your tests here.
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
import time


class ScheduleFactory(object):
    def __init__(self):
        if not hasattr(ScheduleFactory, '__scheduler'):
            __scheduler = ScheduleFactory.get_instance()
        self.scheduler = __scheduler

    @staticmethod
    def get_instance():
        pool = redis.ConnectionPool(
            host='172.16.120.15',
            port=6379,
        )
        r = redis.StrictRedis(connection_pool=pool)
        jobstores = {
            'redis': RedisJobStore(connection_pool=pool),
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        executors = {
            'default': ThreadPoolExecutor(max_workers=30),
            'processpool': ProcessPoolExecutor(max_workers=30)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults,daemonic=False)
        #scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, daemonic=False)
        return scheduler

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()


def print_hello():
    print("Hello,%s" % datetime.now())


schedule = ScheduleFactory().get_instance()
schedule.add_job(print_hello, jobstore='default', trigger='interval', seconds=10, id="jobs14", executor='processpool',
                 misfire_grace_time=30)
#schedule.remove_all_jobs()
schedule.start()

while True:
    time.sleep(10)
    print("A")




# import redis
# import configparser
#
# # CONFIG = configparser.ConfigParser()
# # CONFIG.read("config/system.ini")
# # redis_host = CONFIG.get("redis", "REDIS_HOST")
# # redis_port = CONFIG.get("redis", "REDIS_PORT")
# # redis_db = CONFIG.get("redis", "REDIS_DB")
# # redis_pwd = CONFIG.get("redis", "REDIS_PASSWORD")
#
# redisConnect = redis.Redis("172.16.120.15", 6379)
#
# redisConnect.set("JET", "hahahahahahahahahah")
# print(redisConnect.get("JET"))
#
# class RedisTool:
#     @staticmethod
#     def hexists(name, key):
#         return redisConnect.hexists(name, key)
#
#     @staticmethod
#     def hget(name, key):
#         return redisConnect.hget(name, key)
#
#     @staticmethod
#     def getset(name, value):
#         return redisConnect.getset(name, value)
#
#     @staticmethod
#     def hdel(name, *keys):
#         return redisConnect.hdel(name, *keys)
#
#     @staticmethod
#     def hgetall(name):
#         return redisConnect.hgetall(name)
#
#     @staticmethod
#     def hkeys(name):
#         return redisConnect.hkeys(name)
#
#     @staticmethod
#     def hlen(name):
#         return redisConnect.hlen(name)
#
#         # Set key to value within hash name Returns 1 if HSET created a new field, otherwise 0
#
#     @staticmethod
#     def hset(name, key, value):
#         return redisConnect.hset(name, key, value)
#
#     @staticmethod
#     def setex(name, time, value):
#         return redisConnect.setex(name, time, value)
#
#     @staticmethod
#     def get(name):
#         return redisConnect.get(name)
#
#     @staticmethod
#     def exists(name):
#         return redisConnect.exists(name)
#
#     @staticmethod
#     def set(name, value):
#         return redisConnect.set(name, value)
