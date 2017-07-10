from django.db import models

# Create your models here.

from tinymce.models import HTMLField
# Create your models here.


class TypeInfo(models.Model):
    ttitle=models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=20)
    gpic=models.ImageField(upload_to='goods/')
    gprice=models.DecimalField(max_digits=5,decimal_places=2)
    gclick=models.IntegerField()
    gunit=models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)
    gsubtitle=models.CharField(max_length=200)
    gkucun = models.IntegerField(default=100)
    gcontent=HTMLField()
    gtype=models.ForeignKey('TypeInfo')