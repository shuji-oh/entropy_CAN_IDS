# -+- coding: utf-8 -*-
import random	#Random module
import math

# Ra is detection rate attack blocks 
# Rn is detection rate normal blocks
# Rt is detection time
Ra = 0
Da = 0
Rn = 0
Dn = 0
Rt = 0

# Ta is attack log total, Tn is normal log total
Ta = 1000
Tn = 35000

# Three weighted parameters
C1 = 1
C2 = 0.5
C3 = 1

# define energy function
def function_E(Ra, Rn, Rt):
	global C1
	global C2
	global C3
	return Ra*C1+Rn*C2+Rt*C3

def EntropyBased_IntrusionDetect(Test_Data, k, div, WindowSize):
	canid_list = list()
	w_count = 0
	H_id_i = 0
	H_I = 0

	# calculate Ra, Rn, Rt
	for I in Test_Data:

		# create canid list of WindowSize
		canpacket = I.split("#")
		canid_list.append(canpacket[0])
		id_i += 1

		# if canid_list of WindowSize is created,
		# entropy H_I is calculated.
		if id_i == WindowSize:
			w_count += 1
			id_count = [0 for i in range(2048)]
			for canid in canid_list:
				id_count[int(canid, 16)] += 1

			# calculate H_I
			for canid_i in range(0, 2048):
				if id_count[canid_i] != 0:
					#print("id_i = %x, count = %d" % (canid_i, id_count[canid_i]))
					H_id_i += (float(id_count[canid_i])/W)*(math.log(float(W)/id_count[canid_i])) 
					#print( (id_count[canid_i]/W)*(math.log(W/id_count[canid_i])) )
			H_I = H_id_i

			# perform Intrusion Detection using Sliding Entropy
			if H_I < (ave-k*div) or (ave+k*div) < H_I:
				Da += 1
				Ra = (float(Da*W)/Ta)
				Rt = Current - attack
			else:
				Dn += 1
				Rn = (float(Dn*W)/Tn)

			print("[%d] H_I=%f" % (w_count, H_I))
			H_id_i = 0
			canid_list = []
			id_i = 0

	
	return Ra, Rn, Rt

def SimulatedAnnealing_Optimize(DoS_Data, Tmax=10000):
	# init random value
	#vec = random.randint(-2,2)
	k_best		= 0.6
	div_best	= random.random()
	W_best		= random.random()
	Ra, Rn, Rt 	= EntropyBased_IntrusionDetect(DoS_Data, k_best, div_best, W_best)
	e_best		= function_E(Ra, Rn, Rt)
	T 			= 0

	while T < Tmax and e < e_best:
		# row 7 in paper
		div_next = random.random()
		W_next = random.random()

		# row 8 in paper
		Ra, Rn, Rt = EntropyBased_IntrusionDetect(DoS_Data, k_best, div_next, W_next)
		e_next = function_E(Ra, Rn, Rt)

		# calcurate probability from templature.
		p = pow(math.e, -abs(e_next- e_prev) / T)

		# 変更後のコストが小さければ採用する。
		# コストが大きい場合は確率的に採用する。
		if random.random() < p:
			div_prev 	= div_next
			W_prev 		= W_next
			e_prev 		= e_next
			if e_prev > e_best:
				div_best 	= div_prev
				W_best 		= W_prev
				e_best 		= e_prev

		# update templature
		T = T + 1

	return div_best, W_best

if __name__ == '__main__':
	div, WindowSize = SimulatedAnnealing_Optimize(DoS_Data, Tmax=10000)
	print("Optimazed Param:Deviation=%f, WindowSize=%d" %(div, WindowSize))
