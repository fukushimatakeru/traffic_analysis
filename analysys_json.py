from base import *
import datetime
import csv
import sys
import os
import json

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
first_dateitme_day = first_datetime.day
#last_datetime_str = last_traffic_list[-1]['datetime']
#last_datetime = datetime.datetime.strptime(last_datetime_str[:19], '%Y-%m-%d %H:%M:%S')
#last_datetime_hour = last_datetime.hour

# 解析開始
analysysed_traffics = {}
window_hour = first_datetime_hour + 1
window_day = first_dateitme_day + 1
for json_file_path in json_file_paths:
	print(json_file_path)
	with open(json_file_path, "r") as f:
		traffic_list = json.load(f)
	for traffic_dict in traffic_list:
		# 時間を取得
		t_datetime_str = traffic_dict['datetime']
		t_datetime = datetime.datetime.strptime(t_datetime_str[:19], '%Y-%m-%d %H:%M:%S')
		t_datetime_hour = t_datetime.hour
		t_datetime_day = t_datetime.day

		# log
		sys.stdout.write("\rwh:%i,%s" % (window_hour, t_datetime_str))
		sys.stdout.flush()

		if t_datetime_hour == window_hour:
			# 追加処理
			src = traffic_dict['src']
			dst = traffic_dict['dst']
			size = traffic_dict['size']
			# すでに src が存在
			if src in analysysed_traffics:
				# すでに dst が存在
				if dst in analysysed_traffics[src]:
					pprint(analysysed_traffics[src][dst])
					analysysed_traffics[src][dst] += size
				else:
					analysysed_traffics[src][dst] = size
			else:
				analysysed_traffics[src] = {dst: size}
		elif t_datetime_hour > window_hour:
			# 終了処理
			if window_hour + 1 >23:
				window_hour = 0
				window_day += 1
			output_path = "json/%02i_%02i-%02i.json"%(window_day, window_hour, window_hour+1)
			with open(output_path, "w") as f2:
				print("%sを出力開始。"%output_path)
				json.dump(analysysed_traffics, f2)
				print("%sを出力終了。"%output_path)
			analysysed_traffics = {}
			window_hour += 1
			if window_hour + 1 >23:
				window_hour = 0
				window_day += 1
			# 追加処理
			src = traffic_dict['src']
			dst = traffic_dict['dst']
			size = traffic_dict['size']
			analysysed_traffics[src] = {dst: size}
		else:
			# スキップ処理
			analysysed_traffics = {}
	sys.stdout.write("\r")
	sys.stdout.flush()
#	if window_hour >= last_datetime_hour:
#		print("break")
#		break
