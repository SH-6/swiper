# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag
import qiniu.config

from swiper import config as cfg


def upload_to_qn(local_filepath, upload_filename):
    '''将文件上传到七牛云
    Args:
        local_filepath:本地文件路径
        upload_filename:上传后保存的文件名
    '''

    # 构建鉴权对象
    qn_auth = Auth(cfg.QN_ACCESS_KEY, cfg.QN_SECRET_KEY)

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(cfg.QN_BUCKET, upload_filename, 3600)
    # 要上传文件的本地路径

    ret, info = put_file(token, upload_filename, local_filepath)

    file_url =  '%s/%s' % (cfg.QN_BASE_URL, upload_filename)#上传后的文件链接
    return file_url