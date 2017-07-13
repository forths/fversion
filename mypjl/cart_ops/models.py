from django.db import models
from user_ops.models import UserInfo
# Create your models here.


class CartInfo(models.Model):
    goods = models.ForeignKey('goods_ops.GoodsInfo')
    user = models.ForeignKey(UserInfo)
    count = models.IntegerField()
