import math
w_count = 0
W = 60
k = 0.7
div = 0.7
ave = 3.0
Ra = 0
Ra_count = 0
Rn = 0
Rn_count = 0
Rt = 0
Da = 0
Dn = 0
Ta = 1000
Tn = 57001
C1 = 1
C2 = 0.5
C3 = 1
id_i = 0
H_id_i = 0
H_I = 0
Ta = 0
Tn = 0
canid_list = list()
#with open("1min_CANtraffic.log") as f:

def E ():
	global Ra
	global Rn
	global Rt
	return Ra*C1+Rn*C2+Rt*C3

with open("1min_DoStraffic.log") as f:
#with open("candump-2018-09-22_221913.log") as f:
	for log in f:
		log_split = log.split(" ")
		canpacket = log_split[2].split("#")
		#packet_label = log_split[3]
		canid_list.append(canpacket[0])
		id_i += 1
		if id_i == W:
			w_count += 1
			id_count = [0 for i in range(2048)]
			for canid in canid_list:
				id_count[int(canid, 16)] += 1
			for canid_i in range(0, 2048):
				if id_count[canid_i] != 0:
					#print("id_i = %x, count = %d" % (canid_i, id_count[canid_i]))
					H_id_i += (float(id_count[canid_i])/W)*(math.log(float(W)/id_count[canid_i])) 
					#print( (id_count[canid_i]/W)*(math.log(W/id_count[canid_i])) )
			H_I = H_id_i
			if H_I < (ave-k*div) or (ave+k*div) < H_I:
				Ra_count += 1
				Ta = 1000
				Ra = (float(Ra_count*W)/Ta)
			else:
				Rn_count += 1
				Tn = 57001
				Rn = (float(Rn_count*W)/Tn)
			H_id_i = 0
			print("[%d] H_I=%f" % (w_count, H_I))
			#list clear
			canid_list = []
			id_i = 0
	print("Ra=%f, Rn=%f" % (Ra, Rn))
		#print(log_split[2], end="")
