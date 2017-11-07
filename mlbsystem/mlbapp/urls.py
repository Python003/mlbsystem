# -*- coding:utf-8 -*-

from mlbapp.views import *
from django.conf.urls import url

urlpatterns = [
	url('/getusernum/$',getusernum,name='getusernum'),  #获取查询工号
	url('/loanboard/$',loanboardpage,name='loanboard'),	#借板
	url('/addboard/$',addboard,name='addboard'),		#板子录入
	url('/confirmadd/$',confirmadd,name='confirmadd'),	#确认录入
	url('/backboardpage/$',backboardpage,name='backboardpage'),     #主板归还
	url('/index/$',index,name='index'),					#主页
	url('/loansearch/$',loansearch,name='loansearch'),  #借出查询
	url('/backsearch/$',backsearch,name='backsearch'),  #归还查询
	url('/confirmloan',confirmloan,name='confirmloan'), #确认借板
	url('/pro_cfg_loan/',pro_cfg_loan),
	url('/confirmback/',confirmback),
]

