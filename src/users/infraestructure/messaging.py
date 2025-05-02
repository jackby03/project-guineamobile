from aio_pika.abc import AbstractRobustChannel


class UserCommandPublisher:
    def __init__(self, channel: AbstractRobustChannel):
        self.channel = channel