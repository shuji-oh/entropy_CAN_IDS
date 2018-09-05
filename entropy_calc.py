import math
w_count = 0
W = 50
k = 0.5
div = 0.5
Ra = 0
Rn = 0
Rt = 0
id_i = 0
H_id_i = 0
H_I = 0
canid_list = list()
with open("1min_CANtraffic.log") as f:
	for log in f:
		log_split = log.split(" ")
		canpacket = log_split[2].split("#")
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
			H_id_i = 0
			print("[%d]H_I=%f" % (w_count, H_I))
			#list clear
			canid_list = []
			id_i = 0
		#print(log_split[2], end="")