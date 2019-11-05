import datetime

from django.db import models

from libs.cache import rds

from common.keys import MODEL_KEY


def get(cls, *args, **kwargs):
    """
    Performs the query and returns a single object matching the given
    keyword arguments.
    """
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk is not None:
        model_key = MODEL_KEY % (cls.__name__, pk)  # 定義緩存 key
        # 從緩存獲取對象
        cache_model_obj = rds.get(model_key)
        if isinstance(cache_model_obj, cls):
            return cache_model_obj

    # 緩存沒有,從數據庫獲取
    model_obj = cls.objects.get(*args, **kwargs)

    # 將獲取的對象寫入緩存
    model_key = MODEL_KEY % (cls.__name__, model_obj.pk)
    rds.set(model_key, model_obj)

    return model_obj


def get_or_create(cls, defaults=None, **kwargs):
    """
    Looks up an object with the given kwargs, creating one if necessary.
    Returns a tuple of (object, created), where created is a boolean
    specifying whether an object was created.
    """
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk is not None:
        model_key = MODEL_KEY % (cls.__name__, pk)  # 定義緩存 key
        # 從緩存獲取對象
        cache_model_obj = rds.get(model_key)
        if isinstance(cache_model_obj, cls):
            return cache_model_obj, False

    # 緩存沒有,從數據庫獲取
    model_obj, created = cls.objects.get_or_create(defaults, **kwargs)

    # 將獲取的對象寫入緩存
    model_key = MODEL_KEY % (cls.__name__, model_obj.pk)
    rds.set(model_key, model_obj)

    return model_obj, created


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
    Saves the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    # 将对象写入数据库
    self._save(self, force_insert=False, force_update=False, using=None,
               update_fields=None)

    # 将对象写入缓存
    model_key = MODEL_KEY % (self.__class__.__name__, self.pk)
    rds.set(model_key, self)


def to_dict(self, *ignores, **extend):
    '''将model 装换成一个字典'''
    attr_dict = {}
    for field in self._meta.fields:
        name = field.attname
        # 过滤出需要排除的字段
        if name in ignores:
            continue
        else:
            value = getattr(self, name)
            if isinstance(value, (datetime.date, datetime.time, datetime.datetime)):
                value = str(value)
            attr_dict[name] = value
    # 添加额外的字段
    attr_dict.update(extend)
    return attr_dict


def patch_model():
    '''通过 MonkeyPatch 的方式动态修改 model功能'''
    models.Model.to_dict = to_dict
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    models.Model._save = models.Model.save  # 将原 save改名
    models.Model.save = save  # 将带缓存出来的 save添加到 Model
