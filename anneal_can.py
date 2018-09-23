# -+- coding: utf-8 -*-
import random	#ランダムモジュール
import math

def annealingoptimize(T=10000, cool=0.99, step=1):
	# ランダムな値で初期化
	vec = random.randint(-2,2)

	while T > 0.0001:
		# 変更する変数を一つ選ぶ。
		# 今回の場合は1次元なので選ぶ必要がない。
		# i = random.randint(0, dimmension-1)
	
		# 変数の値を増加させるか、減少させるかを決定する。
		dir = random.random()
		dir = (dir - 0.5) * step

		# 変数の値を変更する。
		newvec = vec + dir

		# 変更前と変更後のコストを計算する。
		newcost = costf(newvec)
		cost = costf(vec)

		# 温度から確率を定義する。
		p = pow(math.e, -abs(newcost - cost) / T)
		print p

		# 変更後のコストが小さければ採用する。
		# コストが大きい場合は確率的に採用する。
		if(newcost < cost or random.random() < p):
			vec = newvec
			
		# 温度を下げる
		T = T * cool

	return vec
	
def costf(x):
	return (3*(x**4)) - (5*(x**3)) + (2*(x**2))

#if __name__ == '__main__':
#	print annealingoptimize()
if __name__ == '__main__':
	success, failure = 0,0
	for i in range(0, 1000):
		ans = annealingoptimize()
		if (ans >= -0.05 and ans <= 0.05):
			failure += 1
		if (ans > 0.8 and ans <= 0.9):
			success += 1
	
	print success,failure