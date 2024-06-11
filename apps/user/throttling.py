from rest_framework import throttling


class SendFriendRequestThrottling(throttling.UserRateThrottle):
    rate = '3/min'
    THROTTLE_RATES = {
        'rate': '3/min'
    }
