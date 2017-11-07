# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mlbapp.models import *
# Register your models here.

class userAdmin(admin.ModelAdmin):
	list_display = ('userid','usernum','username')

class pro_cfgAdmin(admin.ModelAdmin):
	list_display = ('pro_cfg','totalnums','loannums','remainnums')

class boardAdmin(admin.ModelAdmin):
	list_display = ('boardid','boardcode','sn','config','source','teststatus','storetime','status',)

admin.site.register(user,userAdmin)
admin.site.register(pro_cfg,pro_cfgAdmin)
admin.site.register(board,boardAdmin)