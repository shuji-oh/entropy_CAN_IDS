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
#with open("1min_CANtraffic.log") as f:
#with open("1min_TargetedDoStraffic.log") as f:
with open("candump-2018-09-22_221913.log") as f:
    for log in f:
        log_split = log.split(" ")
        canpacket = log_split[2].split("#")
        #print(format(int(canpacket[0], 16),'011b'))
        canpacket_bin = format(int(canpacket[0], 16),'011b')
        #print(canpacket_bin)
        canid_list.append(canpacket_bin)
        id_i += 1
        if id_i == W:
            w_count += 1
            id_count = [0 for i in range(11)]
            for canid in canid_list:
                if canid[0] == "1":
                    id_count[0] += 1
                elif canid[1] == "1":
                    id_count[1] += 1
                elif canid[2] == "1":
                    id_count[2] += 1
                elif canid[3] == "1":
                    id_count[3] += 1
                elif canid[4] == "1":
                    id_count[4] += 1
                elif canid[5] == "1":
                    id_count[5] += 1
                elif canid[6] == "1":
                    id_count[6] += 1
                elif canid[7] == "1":
                    id_count[7] += 1
                elif canid[8] == "1":
                    id_count[8] += 1
                elif canid[9] == "1":
                    id_count[9] += 1
                elif canid[10] == "1":
                    id_count[10] += 1
            for canid_i in range(0, 11):
                if id_count[canid_i] != 0:
                    #print("id_i = %x, count = %d" % (canid_i, id_count[canid_i]))
                    H_id_i += (float(id_count[canid_i])/W)*(math.log(float(W)/id_count[canid_i])) 
                    #print( (id_count[canid_i]/W)*(math.log(W/id_count[canid_i])) )
            H_I = H_id_i
            H_id_i = 0
            print("[%d] H_I=%f" % (w_count, H_I))
            #list clear
            canid_list = []
            id_i = 0
        #print(log_split[2], end="")
