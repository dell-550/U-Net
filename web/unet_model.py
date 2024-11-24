from unet import Unet


class Singleton:
    _instance = None  # 用于存储单例实例

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:  # 如果实例不存在，则创建一个
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

class UNetModel(Singleton):
    net = None

    def get_net(self):
        if self.net:
            return self.net
        else:
            self.net = Unet()
            return self.net