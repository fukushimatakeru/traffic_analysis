from base import *
import datetime
import csv
import sys
import os
import json
import codecs

# コマンドライン入力
args = sys.argv
if len(args) <= 2:
	print('python analysys_json.py [start_num] [end_num]')
	exit()

# 引数を取得
for i, arg in enumerate(args):
	if i == 1:
		start_num = int(arg)
	elif i == 2:
		end_num = int(arg)

# ファイルパスを全取得
json_file_paths = []
for i in range(start_num, end_num+1):
	json_file_path = "json/capture_%03i.PCAP.json"%i
	json_file_paths.append(json_file_path)

pprint(json_file_paths)

# ファイルをロード
with open(json_file_paths[0], "r") as f:
	first_traffic_list = json.load(f)
#with open(json_file_paths[-1], "r") as f:
#	last_traffic_list = json.load(f)

# 最初と最後のdatetimeを取得
first_datetime_str = first_traffic_list[0]['datetime']
first_datetime = datetime.datetime.strptime(first_datetime_str[:19], '%Y-%m-%d %H:%M:%S')
first_datetime_hour = first_datetime.hour
first_datetime_minute = first_datetime.minute
first_datetime_day = first_datetime.day
#last_datetime_str = last_traffic_list[-1]['datetime']
#last_datetime = datetime.datetime.strptime(last_datetime_str[:19], '%Y-%m-%d %H:%M:%S')
#last_datetime_hour = last_datetime.hour

analysysed_traffics = {}
window_minute = first_datetime_minute + 1
window_hour = first_datetime_hour + 1
# window_day = first_dateitme_day + 1
for json_file_path in json_file_paths:
	print(json_file_path)
	with open(json_file_path, "r") as f:
		traffic_list = json.load(f)
	for traffic_dict in traffic_list:
		# 時間を取得
		t_datetime_str = traffic_dict['datetime']
		t_datetime = datetime.datetime.strptime(t_datetime_str[:19], '%Y-%m-%d %H:%M:%S')
		t_datetime_minute = t_datetime.minute
		t_datetime_hour = t_datetime.hour
	#	t_datetime_day - t_datetime.day
		sys.stdout.write("\r%d" % t_datetime_minute)
		sys.stdout.flush()
		if t_datetime_hour == window_hour:
			# 追加処理
			hour = traffic_dict['t_datetime_hour']
			minute = traffic_dict['t_datetime_minute']
			size = traffic_dict['size']
			# すでに hour が存在
			if hour in analysysed_traffics:
				# すでに minute が存在
				if minute in analysysed_traffics[hour]:
					pprint(analysysed_traffics[hour][minute])
					analysysed_traffics[hour][minute] += size
				else:
					analysysed_traffics[hour][minute] = size
			else:
				analysysed_traffics[hour] = {minute: size}
		elif t_datetime_minute > window_minute:
			output_path = "json/%02i_%02i-%02i.json"%(window_hour, window_minute, window_minute+1)
			with open(output_path, "w") as f2:
				print("%sを出力開始。"%output_path)
				json.dump(analysysed_traffics, f2)
				print("%sを出力終了。"%output_path)
		#	analysysed_traffics = {}
			window_minute += 1
			'''
			if window_minute + 1 > 59:
				window_minute = 0
				window_hour +=1
				if window_hour + 1 > 23:
					window_hour = 0
			# 追加処理
			hour = traffic_dict['t_datetime_hour']
			minute = traffic_dict['t_datetime_minute']
			size = traffic_dict['size']
			analysysed_traffics[src] = {dst: size}
		else:
		 # スキップ処理
			analysysed_traffics = {}
			'''
	sys.stdout.write("\r")
	sys.stdout.flush()
#	if window_hour >= last_datetime_hour:
#		print("break")
#		break
