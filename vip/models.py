from django.db import models



class Vip(models.Model):
    '''VIP表'''
    name = models.CharField(max_length=16, unique=True, verbose_name='会员名称')
    level = models.IntegerField(verbose_name='会员等级')


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=16, unique=True, verbose_name='权限名称')
    desc = models.TextField(verbose_name='权限说明')

    def perms(self):
        '''当前会员拥有的所有权限'''
        # 先取出对应的权限 ID列表
        perm_id_list = VipPermRelation.objects.filter(
            vip_id=self.id).values_list('perm_id', flat=True)

        # 取出对应的权限
        return Permission.objects.filter(id__in=perm_id_list)

    def has_perm(self, perm_name):
        '''检查当前VIP是否拥有某权限'''
        for perm in self.perms():
            if perm.name == perm_name:
                return True
        return False

class VipPermRelation(models.Model):
    '''会员-权限 的关系表'''
    vip_id = models.IntegerField(verbose_name='会员id')
    perm_id = models.IntegerField(verbose_name='权限 id')


class VipProduct(models.Model):
    '''购买会员的购买项'''
    vip_id = models.IntegerField(verbose_name='对应的 VIP 的ID')
    price = models.FloatField(verbose_name='价格')
    days = models.IntegerField(verbose_name='会员天数')
