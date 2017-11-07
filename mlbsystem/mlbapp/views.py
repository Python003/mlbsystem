# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import request,HttpResponse
from django.db.models import Q
from mlbapp.models import *
import json,datetime

# Create your views here.

def index(request):
	board_list = board.objects.all().order_by('-boardid')
	for b in board_list:
		if b.status != '0':
			loanboard_list = loanboard.objects.filter(board=b)
			length = len(loanboard_list)
			username = loanboard_list[length-1].user.username
			b.status = username
	return render(request,'index.html',{'nav':'index','board_list':board_list})

def loansearch(request):
	loanboard_list = loanboard.objects.all().order_by('-id')
	return render(request,'loansearch.html',{'nav':'loansearch','loanboard_list':loanboard_list})

def loanboardpage(request):
	pro_cfg_list = pro_cfg.objects.all()
	return render(request,'loanboard.html',{'nav':'loanboard','pro_cfg_list':pro_cfg_list,'addorloan':True})

def addboard(request):
	pro_cfg_list = pro_cfg.objects.all()
	return render(request,'addboard.html',{'nav':'addboard','pro_cfg_list':pro_cfg_list,'addorloan':True})

def backsearch(request):
	backboard_instance_list = backboard.objects.all().order_by('-id')
	return render(request,'backsearch.html',{'backboard_instance_list':backboard_instance_list,'nav':'backsearch','addorloan':False})

def backboardpage(request):
	pro_cfg_list = pro_cfg.objects.all()
	return render(request,'backboard.html',{'nav':'backboard','pro_cfg_list':pro_cfg_list,'addorloan':True})

def confirmback(request):
	boardlist = request.GET.get('boardlist')[1:-1].replace('\"','').split(',')
	remark = request.GET.get('remark')
	validateresult = validatebackboard(boardlist)
	result = validateresult['result']
	if not result:
		return HttpResponse(json.dumps({'result':False,'errormsg':validateresult['errormsg']}))
	else:
		boardlist = validateresult['boardlist']
		mlb_instance_list = [mlb for b in boardlist for mlb in board.objects.all() if b == mlb.config]
		loanboard_instance_list = [loanboard_instance for mlb in mlb_instance_list for loanboard_instance in loanboard.objects.all() if mlb == loanboard_instance.board]
		#修改pro_cfg表
		pro_cfg_list = [mlb.pro_cfg for mlb in mlb_instance_list]
		for pro_cfg_instance in pro_cfg_list:
			pro_cfg_instance.loannums = pro_cfg_instance.loannums - 1
			pro_cfg_instance.remainnums = pro_cfg_instance.remainnums + 1
			pro_cfg_instance.save()
		#修改board表status
		for mlb in mlb_instance_list:
			mlb.status = '0'
			mlb.save()
		#增加一条归还记录
		for loanboard_instance in loanboard_instance_list:
			user_instance = loanboard_instance.user
			board_instance = loanboard_instance.board
			backboard_instance = backboard(user=user_instance,board=board_instance,remark=remark)
			backboard_instance.save()
		#删除loanboard借出记录
		for loanboard_instance in loanboard_instance_list:
			loanboard_instance.delete()

	return HttpResponse(json.dumps({'result':True}))

#板号验证与去重
def validatebackboard(boardlist):
	configlist = []
	mlblist = board.objects.all()
	for one in boardlist:
		configflag = False
		for two in mlblist:
			if one == two.config or one == two.sn:
				if two.status == '1':
					configflag = True
					if two.config not in configlist:
						configlist.append(two.config)
					else:
						break
		if not configflag:
			return {'result':False,'errormsg':'%s 不存在或未借出'}
	return {'result':True,'boardlist':configlist}

#确认添加主板
def confirmadd(request):
	boardcode = request.GET.get('boardcode')
	sn = request.GET.get('sn')
	config = request.GET.get('config')
	source = request.GET.get('source')
	teststatus = request.GET.get('teststatus')
	storetime = datetime.datetime.now()
	status = 0

	#验证SN或Config编号是否已经录入
	board_list = board.objects.all()
	errormsg = False
	for b in board_list:
		if sn == b.sn:
			errormsg = 'sn:' + sn  +' 已经录入，不能重复录入！'
			break
		elif config == b.config:
			errormsg = 'config:' + config + ' 已经录入，不能重复录入！'
			break
	if errormsg:
		return HttpResponse(json.dumps({'result':False,'errormsg':errormsg}))

	procfg = config.split('-')[0] + '_' + config.split('_')[-2]
	pro_cfg_list = pro_cfg.objects.filter(pro_cfg = procfg)
	try:
		if not pro_cfg_list:
			pro_cfg_object = pro_cfg(pro_cfg=procfg,totalnums=1,loannums=0,remainnums=1)
			pro_cfg_object.save()
		else:
			pro_cfg_object = pro_cfg.objects.get(pro_cfg=procfg)
			totalnums = pro_cfg_object.totalnums + 1
			remainnums = pro_cfg_object.remainnums + 1
			pro_cfg_object.totalnums = totalnums
			pro_cfg_object.remainnums = remainnums
			pro_cfg_object.save()

		board_object = board.objects.create(boardcode=boardcode,sn=sn,config=config,source=source,teststatus=teststatus,
							storetime = storetime,status=status,pro_cfg=pro_cfg_object)
	except Exception as e:
		print e
		return HttpResponse(json.dumps({'result':False}))

	return HttpResponse(json.dumps({'result':True}))

#获取查询工号
def getusernum(request):
	sc = request.GET.get('sc')
	userobjectlist = user.objects.filter(Q(usernum__icontains = sc))
	if userobjectlist:
		userlist = []
		for u in userobjectlist:
			userlist.append({'usernum':u.usernum,'username':u.username})
		data = {'result':True,'userlist':userlist}
	else:
		data = {'result':False}
	return HttpResponse(json.dumps(data))

#将主板编号统一转化为config编号
def getconfiglist(boardlist):
	configlist = []
	boardlist = boardlist[1:-1].replace('\"','').split(',')
	mlblist = board.objects.all()
	for one in boardlist:
		configflag = False
		for two in mlblist:
			if one == two.config or one == two.sn:
				if two.status == '0' and two.config  not in configlist:
					configflag = True
					configlist.append(two.config)
				elif two.status == '1':
					return {'result':False,'errormsg':'%s已经借出！' % one}
				break
		if not configflag:
			return {'result':False,'errormsg':'%s未录入！' % one}
	return {'result':True,'configlist':configlist}


#确认借板
def confirmloan(request):
	usernum = request.GET.get('usernum')
	boardlist = request.GET.get('boardlist')
	remark = request.GET.get('remark')
	configresult = getconfiglist(boardlist)
	user_list = user.objects.filter(usernum=usernum)
	if not user_list:
		return HttpResponse(json.dumps({'result':False,'errormsg':'工号不存在！'}))
	if not configresult['result']:
		return HttpResponse(json.dumps({'result':False,'errormsg':configresult['errormsg']}))
	else:
		configlist = configresult['configlist']
		for config in configlist:
			#操作pro_cfg表
			procfg = config.split('-')[0] + '_' + config.split('_')[1]
			pro_cfg_object = pro_cfg.objects.get(pro_cfg=procfg)
			if pro_cfg_object.remainnums > 0:
				pro_cfg_object.loannums += 1
				pro_cfg_object.remainnums -= 1
				pro_cfg_object.save()
			#更新board表
			board_object = board.objects.get(config=config)
			board_object.status = '1'
			board_object.save()
			#更新loanboard表
			user_object = user.objects.get(usernum=usernum)
			loantime = datetime.datetime.now()
			loanboard_object = loanboard.objects.create(user=user_object,loantime=loantime,board=board_object)
			loanboard_object.save()
	return HttpResponse(json.dumps({'result':True}))

def pro_cfg_loan(request):
	from django.core import serializers

	pro_cfg_code = request.GET.get('pro_cfg_code')
	pro_cfg_instance = pro_cfg.objects.get(pro_cfg = pro_cfg_code)
	board_list = board.objects.filter(pro_cfg=pro_cfg_instance,status='1')
	loanboard_list = []
	for board_instance in board_list:
		for one in loanboard.objects.filter(board=board_instance,isback=False):
			loanboard_list.append(one)
	data = {'result':True,'loanboard_list':loanboard_list}
	return render(request,'pro_cfg_detail.html',data)