from rest_framework import status
from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache as default_cache
from rest_framework import exceptions
from app1.extensions import return_code


class ThrottledException(exceptions.APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 'throttled'


class NewsCreateRateThrottle(SimpleRateThrottle):
    cache = default_cache  # 访问记录存放在django的缓存中（需设置缓存）
    scope = "user"  # 构造缓存中的key
    cache_format = 'throttle_%(scope)s_%(ident)s'

    # 设置访问频率，例如：1/5m
    THROTTLE_RATES = {"user": "1/5m"}

    def parse_rate(self, rate):
        if rate is None:
            return (None, None)
        num, period = rate.split('/')  # "1/5m"
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[-1]]
        count = int(period[0:-1])
        return (num_requests, duration * count)

    def get_cache_key(self, request, view):
        ident = request.user.pk
        return self.cache_format % {'scope': self.scope, 'ident': ident}

    def throttle_failure(self):
        wait = self.wait()
        detail = {
            "code": return_code.TOO_MANY_REQUESTS,
            "data": "访问频率限制",
            'detail': "需等待{}秒后才能访问".format(int(wait))
        }
        raise ThrottledException(detail)

    def throttle_success(self):
        # self.history.insert(0, self.now)
        # self.cache.set(self.key, self.history, self.duration)
        return True

    def done(self):
        """ 数据库中创建成功后，再来调用这个方法"""
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
