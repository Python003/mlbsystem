# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.

class user(models.Model):                          #用户表
	userid = models.AutoField(primary_key=True)
	usernum = models.CharField(max_length=20)
	username = models.CharField(max_length=20)

	def __str__(self):
		return self.usernum

class pro_cfg(models.Model):
	pro_cfg = models.CharField(max_length=20)
	totalnums = models.IntegerField()              #总数量
	loannums = models.IntegerField()               #借出数量
	remainnums = models.IntegerField()             #剩余数量

class board(models.Model):                         #主板表
	boardid = models.AutoField(primary_key=True)
	boardcode = models.CharField(max_length=20)    #编码
	sn = models.CharField(max_length=20)           #sn编号
	config = models.CharField(max_length=50)       #config编号
	source = models.CharField(max_length=20)       #板子来源
	teststatus = models.CharField(max_length=30)   #测试状态
	storetime = models.DateTimeField()             #入库时间
	status = models.CharField(max_length=20)       #状态 0:在库，1:借出
	pro_cfg = models.ForeignKey(pro_cfg)

	def __str__(self):
		return self.config

class loanboard(models.Model):                     #借板登记表
	board = models.ForeignKey(board)
	user = models.ForeignKey(user)                 #借板人
	loantime = models.DateTimeField()              #借板时间
	remark = models.TextField(default='')          #备注
	isback = models.BooleanField(default=False)    #是否已经归还
	
class backboard(models.Model):
	board = models.ForeignKey(board)
	user = models.ForeignKey(user)
	backtime = models.DateTimeField(default=datetime.now())             #还板时间
	remark = models.TextField(null=True,blank=True)						#备注

class delboard(models.Model):
	board = models.ForeignKey(board)
	deltime = models.DateTimeField()              #删板时间