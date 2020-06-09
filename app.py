# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify, redirect, send_from_directory, url_for
import random
import requests
import os
app = Flask(__name__)

#ホーム 名前入力
@app.route("/")
def home():	
	return render_template('home.html')

#厳選結果を表示
@app.route("/result/",methods=['POST','GET'])
def result():
	result = []
	if request.method == "GET":	#結果URLから読み込むときはGETでパラメータを受ける
		name = request.args.get("name",default="")
		count = int(request.args.get("count",default="1"))
		result.append(int(request.args.get("h",default="99")))
		result.append(int(request.args.get("a",default="99")))
		result.append(int(request.args.get("b",default="99")))
		result.append(int(request.args.get("c",default="99")))
		result.append(int(request.args.get("d",default="99")))
		result.append(int(request.args.get("f",default="99")))
		result.append(request.args.get("chara",default="おだやかな"))
		result.append(getEvaluation(result))
		if result[0] == 99:	#メソッドがgetだけどパラメータが与えられてなければランダム取得
			result = getRand(name)

	else:	#POSTで受けるのが標準の動き。カウントと名前を受け取り結果はランダム
		count=int(request.form['count'])
		name=request.form['name']
		result = getRand(name)

	if name == "" :	#名前が入力されてなければけつばん
		name = "けつばん"
	#Tweet用URL GETでパラメータを持たす
	url = "https://yourkotaichi.herokuapp.com/result/?"+"name="+name+"&count="+str(count)+"&h="+str(result[0])+"&"+"a="+str(result[1])+"&"+"b="+str(result[2])+"&"+"c="+str(result[3])+"&"+"d="+str(result[4])+"&"+"f="+str(result[5])+"&"+"chara="+result[6]
	short_url = get_shortenURL(url)
	return render_template('result.html', name=name,count=count,result=result,url=short_url)

#個体値・性格・総合評価を取得
def getRand(name):
	individual_value = []
	if name == "ねこ":	#ねこは最強なので6V
		for num in range(6):
			individual_value.append(31)			
	else:
		for num in range(6):	#6値ランダム生成(ちょっとVでやすい)
			num = random.randrange(0,35)
			if num >= 31:
				num = 31
			individual_value.append(num)

	individual_value.append(getCharacter(random.randrange(0,24)))	#性格ランダム生成
	individual_value.append(getEvaluation(individual_value))			#個体値総合評価取得
	getSyuzoku(name)	#種族値取得
	return individual_value

#乱数をもとに性格を返す
def getCharacter(char_num):
	if char_num == 0:
		character="さみしがりな"
	elif char_num == 1:
		character="いじっぱりな"
	elif char_num == 2:
		character="やんちゃな"
	elif char_num == 3:
		character="ゆうかんな"
	elif char_num == 4:
		character="ずぶとい"
	elif char_num == 5:
		character="わんぱくな"
	elif char_num == 6:
		character="のうてんきな"
	elif char_num == 7:
		character="のんきな"
	elif char_num == 8:
		character="ひかえめな"
	elif char_num == 9:
		character="おっとりした"
	elif char_num == 10:
		character="うっかりやな"
	elif char_num == 11:
		character="れいせいな"
	elif char_num ==12:
		character="おだやかな"
	elif char_num == 13:
		character="おとなしい"
	elif char_num == 14:
		character="しんちょうな"
	elif char_num == 15:
		character="なまいきな"
	elif char_num == 16:
		character="おくびょうな"
	elif char_num == 17:
		character="せっかちな"
	elif char_num == 18:
		character="ようきな"
	elif char_num == 19:
		character="むじゃきな"
	elif char_num == 20:
		character="てれやな"
	elif char_num == 21:
		character="がんばりやな"
	elif char_num == 22:
		character="すなおな"
	elif char_num == 23:
		character="きまぐれな"
	else:
		character="まじめな"
	return character

#個体値総合評価
def getEvaluation(indi):
	sumindi = 0		#個体値合計
	v = 0			#Vの数
	zero = 0		#0の数
	for num in range(6):
		sumindi = sumindi + indi[num]
		if indi[num] == 31:
			v+=1
		if indi[num] == 0:
			zero+=1
	eval = getFirstEvaluation(v,zero) + getSecondEvaluation(sumindi)
	return eval

#0,Vの数をもとに評価前半を決定
def getFirstEvaluation(v,zero):
	if v == 3:
		firstEval = "3V。"
	elif v == 4:
		firstEval = "4Vおめでとう！"
	elif v == 5:
		firstEval = "前人未到の5V達成！"
	elif v == 6:
		firstEval = "世界最強"
	else:
		firstEval = ""

	if zero >= 2 and v >= 2:
		firstEval = "ピーキーすぎる。"
	elif zero >= 2:
		firstEval = "汚点が目立つ。"

	return firstEval

#個体値合計をもとに評価後半を決定
def getSecondEvaluation(sumindi):
	if 186 > sumindi > 176:
		secondEval = "世界レベル。"
	elif sumindi == 186:
		secondEval = ""
	elif 176 >= sumindi > 166:
		secondEval = "100年に1匹の逸材。"
	elif 166 >= sumindi > 156:
		secondEval = "地球人最強クラス。"
	elif 156 >= sumindi > 146:
		secondEval = "好き。"
	elif 146 >= sumindi > 136:
		secondEval = "とてもつよい。"
	elif 136 >= sumindi > 126:
		secondEval = "なかなかやるね。"
	elif 126 >= sumindi > 116:
		secondEval = "及第点かな。"
	elif 116 >= sumindi > 106:
		secondEval = "特に印象に残らない。"
	elif 106 >= sumindi > 96:
		secondEval = "ふーん。"
	elif 96 >= sumindi > 86:
		secondEval = "ぱっとしない。"
	elif 86 >= sumindi > 76:
		secondEval = "話にならない。"
	elif 76 >= sumindi > 66:
		secondEval = "来世に期待。"
	elif 66 >= sumindi > 56:
		secondEval = "はなくそ。"
	elif 56 >= sumindi > 46:
		secondEval = "ポッポ以下。"
	elif 46 >= sumindi > 36:
		secondEval = "才能が無い。"
	elif 36 >= sumindi > 26:
		secondEval = "とてもよわい。"
	elif 26 >= sumindi > 16:
		secondEval = "義務教育からやりなおせ。"
	else:
		secondEval = "無能オブ無能。"
	return secondEval


#種族値を取得(今のとこ表示だけ、値も適当。名前によって一意に決定する)
def getSyuzoku(name):
	syuzoku_value = []
	random.seed(name)
	for num in range(6):
		num = random.randrange(0,130)
		syuzoku_value.append(num)
	print("種族値:")
	print(syuzoku_value)



def get_shortenURL(longUrl):
	api_key = 'AIzaSyCSezSC2JFEXUBRaDeZGwMISk7Gwcms6PE'
	url = "https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key="+ api_key
	data = {
    	"dynamicLinkInfo": {
        	"dynamicLinkDomain": "yourkotaichi.page.link",
       		"link": longUrl,
    	}
	}
	result = requests.post(url, json=data)
	shortUrl = result.json()['shortLink']
	return shortUrl

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000)
