# -+- coding: utf-8 -*-
import sys
import random	#Random module
import math

# Ta is attack log total packet num, Tn is normal log total packet num
#Ta_packet = 1000
#Tn_packet = 57001
Ta_packet = 1000
Tn_packet = 1000

# Three weighted parameters
C1 = 1
C2 = 0.5
C3 = 1

# define energy function
def function_E(Ra, Rn, Rt):
	global C1
	global C2
	global C3
	return Ra*C1-Rn*C2-Rt*C3

def EntropyBased_IntrusionDetect(Test_Data, k, div, WindowSize):
	
	# Ra is detection rate attack blocks 
	# Rn is detection rate normal blocks
	# Rt is detection time
	Ra = 0
	Rn = 0
	Rt = 0
	Da = 0
	Dn = 0
	ave = 3.0
	w_count = 0
	H_id_i = 0
	H_I = 0
	id_i = 0
	True_count = 0
	False_count = 0
	canid_list = list()
	labels = list()
	global Ta_packet
	global Tn_packet
	Ta = Ta_packet/WindowSize
	Tn = Tn_packet/WindowSize
	
	
	with open(Test_Data) as Is:
		# calculate Ra, Rn, Rt
		for I in Is:

			# create canid list of WindowSize
			I_spt =	I.split(" ")
			canpacket = I_spt[1].split("#")
			canid_list.append(canpacket[0])
			if I_spt[0] == "1":
				True_count += 1
			else:
				False_count += 1
			#print(labels)
			#print(canpacket[0])
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
						H_id_i += (float(id_count[canid_i])/WindowSize)*(math.log(float(WindowSize)/id_count[canid_i])) 
						#print( (id_count[canid_i]/W)*(math.log(W/id_count[canid_i])) )
				H_I = H_id_i

				# perform Intrusion Detection using Sliding Entropy
				if H_I < (ave-k*div) or (ave+k*div) < H_I:
					# True Positive
					if True_count > False_count:
						Da += 1
						Ra = (float(Da)/Ta)*100
					# False Positive
					else:
						Dn += 1
						Rn = (float(Dn)/Tn)*100

				#print("[%d] H_I=%f" % (w_count, H_I))
				H_id_i = 0
				canid_list = []
				id_i = 0
				True_count = 0
				False_count = 0
	#print("W=%d, Ta=%d, Tn=%d, Da=%d, Dn=%d"%(WindowSize, Ta, Tn, Da, Dn))
	return Ra, Rn, Rt

def SimulatedAnnealing_Optimize(DoS_Data, T=10000, cool=0.99):
	# init random value
	#vec = random.randint(-2,2)
	k_best		= 1.0
	div_best	= random.random()
	W_best		= random.randint(5,70)
	Ra, Rn, Rt 	= EntropyBased_IntrusionDetect(DoS_Data, k_best, div_best, W_best)
	e_best		= function_E(Ra, Rn, Rt)
	e_prev 		= function_E(Ra, Rn, Rt)-1
	#print("E_best=%f"%e_best)
	print("init Param:Deviation=%f, WindowSize=%d" %(div_best, W_best))
	print("Ra=%f,Rn=%f,Rt=%f"%(Ra,Rn,Rt))

	while T > 0.0001 and e_prev < e_best:
		# row 7 in paper
		div_next = random.random()
		W_next = random.randint(W_best-10,W_best+10)

		# row 8 in paper
		Ra, Rn, Rt = EntropyBased_IntrusionDetect(DoS_Data, k_best, div_next, W_next)
		e_next = function_E(Ra, Rn, Rt)
		print("Ra=%f,Rn=%f,Rt=%f"%(Ra,Rn,Rt))
		#print("E=%f,E_best=%f"%(e_next,e_best))

		# calcurate probability from templature.
		p = pow(math.e, -abs(e_next - e_prev)/float(T))
		#print("[%f]Probability=%f"%(T, p))

		# row 9 in paper
		if random.random() < p:
			div_prev 	= div_next
			W_prev 		= W_next
			e_prev 		= e_next
			if e_prev > e_best:
				div_best 	= div_prev
				W_best 		= W_prev
				e_best 		= e_prev

		# cool down
		T = T * cool

	return div_best, W_best

if __name__ == '__main__':
	argvs = sys.argv
	argc = len(argvs)
	if argc < 2:
		print('Usage: python3 %s filename' % argvs[0])
		print('[filename format]\n\t[label] [CAN ID]#[PAYLOAD]\nex)\t1 000#00000000')
		quit()

	DoS_Data = argvs[1]
	div, WindowSize = SimulatedAnnealing_Optimize(DoS_Data, T=10000, cool=0.99)
	print("Optimazed Param:Deviation=%f, WindowSize=%d" %(div, WindowSize))
