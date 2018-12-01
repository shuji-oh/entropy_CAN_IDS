import math
import sys
w_count = 0

W = 60
k = 1.0
div = 0.507669
ave = 3.0

Ra = 0
Da = 0
Rn = 0
Dn = 0
Rt = 0

Ta = 1
Tn = 1000

C1 = 1
C2 = 0.5
C3 = 1

id_i = 0
H_id_i = 0
H_I = 0

Max_H_I = 0.0
Min_H_I = 1000.0
Ave_H_I = 0.0

Packet_count = 0
canid_list = list()

True_count = 0
False_count = 0

def E ():
	global Ra
	global Rn
	global Rt
	return Ra*C1-Rn*C2-Rt*C3

argvs = sys.argv
argc = len(argvs)
if argc < 2:
	print('Usage: python3 %s filename' % argvs[0])
	print('[filename format]\n\t[label] [CAN ID]#[PAYLOAD]\nex)\t1 000#00000000')
	quit()

Data = argvs[1]

with open(Data) as f:
	for log in f:
		log_split = log.split(" ")
		range_entropy = int(log_split[0])
		canpacket = log_split[2]
		canid_list.append(canpacket)
		#print(canpacket)
		id_i += 1
		Packet_count += 1

		if log_split[0] == "1":
				True_count += 1
		else:
				False_count += 1

		if id_i == W:
			w_count += 1
			id_count = [0 for i in range(2048)]
			for canid in canid_list:
				#print(canid)
				id_count[int(canid, 16)] += 1
			for canid_i in range(0, 2048):
				if id_count[canid_i] != 0:
					H_id_i += (float(id_count[canid_i])/W)*(math.log(float(W)/id_count[canid_i])) 
			H_I = H_id_i
			print("%d %f" % (range_entropy, H_I))

			'''
			if H_I < (ave-k*div) or (ave+k*div) < H_I:
				# True Positive
				if True_count > False_count:
					Da += 1
					Ra = (float(Da)/Ta)*100
				# False Positive
				else:
					Dn += 1
					Rn = (float(Dn)/Tn)*100
			
			print("%d %f" % (w_count, H_I))
			if H_I > Max_H_I:
				Max_H_I = H_I
			if H_I < Min_H_I:
				Min_H_I = H_I
			Ave_H_I += H_I
			'''

			#list clear
			canid_list = []
			H_id_i = 0
			id_i = 0

	#print("Ra=%f,Rn=%f,Rt=%f"%(Ra,Rn,Rt))
	#print("Max H_I=%f, Min H_I=%f, Ave H_I=%f" % (Max_H_I, Min_H_I, Ave_H_I/(float(w_count))))