# -+- coding: utf-8 -*-
import sys
import random	#Random module
import math

# Ta is attack log total packet num, Tn is normal log total packet num
#Ta_packet = 1000
#Tn_packet = 57001
Ta_packet = 1000
Tn_packet = 1000

def EntropyBased_IntrusionDetect(Test_Data, k, ave, div, WindowSize):
	
	# Ra is detection rate attack blocks 
	# Rn is detection rate normal blocks
	# Rt is detection time
	TPR = 0
	TNR = 0
	FNR = 0
	FPR = 0
	Da = 0
	Dn = 0
	Na = 0
	Nn = 0
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
						TPR = (float(Da)/Ta)*100
					# False Positive
					else:
						Dn += 1
						FPR = (float(Dn)/Tn)*100
				else :
					# False Negative
					if True_count > False_count:
						Na += 1
						FNR = (float(Na)/Ta)*100
					# True Negative
					else:
						Nn += 1
						TNR = (float(Nn)/Tn)*100


				#print("[%d] H_I=%f" % (w_count, H_I))
				H_id_i = 0
				canid_list = []
				id_i = 0
				True_count = 0
				False_count = 0
	#print("W=%d, Ta=%d, Tn=%d, Da=%d, Dn=%d"%(WindowSize, Ta, Tn, Da, Dn))
	return TPR, FPR, FNR, TNR

if __name__ == '__main__':
	argvs = sys.argv
	argc = len(argvs)
	if argc < 4:
		print('Usage: python3 %s filename average deviation window_size' % argvs[0])
		print('[filename format]\n\t[label] [CAN ID]#[PAYLOAD]\nex)\t1 000#00000000')
		quit()

	DoS_Data = argvs[1]
	ave = float(argvs[2])
	deviation = float(argvs[3])
	W = int(argvs[4])
	#div, WindowSize = SimulatedAnnealing_Optimize(DoS_Data, T=10000, cool=0.99)
	#print("Optimazed Param:Deviation=%f, WindowSize=%d" %(div, WindowSize))
	TP, FP, FN, TN = EntropyBased_IntrusionDetect(DoS_Data, 1.0, ave, deviation, W)
	#print("TP=%f, FP=%f, FN=%f, TN=%f, Recall=%f" %(TP, FP, FN, TN, float(TP)/(TP+FN)))
	print("%f," %(100*float(TP)/(TP+FN)))