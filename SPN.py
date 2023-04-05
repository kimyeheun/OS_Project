print("SPN(Shortest-Process_Next)")
num_process = int(input("프로세스의 수를 입력하세요 : "))
P = dict()          # 프로세스 딕셔너리
'''
P = {"P1" : [idx, AT, BT] ...} 이런 형태로 저장
'''
 
for i in range(num_process):
    key = "P"+str(i+1)
    idx = i     # 인덱스 (P1의 인덱스는 0, P2는 1 ...)
    AT = int(input("P"+str(i+1)+"의 Arrival time을 입력하세요 : "))
    BT = int(input("P"+str(i+1)+"의 Burst time을 입력하세요 : "))
    idx_at_bt = []      # at와 bt가 담기는 배열
    idx_at_bt.append(i)
    idx_at_bt.append(AT)
    idx_at_bt.append(BT)
    idx_at_bt.append(0) # 프로세서가 돌아갔는지 아닌지 확인하기 위한 용도
    P[key] = idx_at_bt
   
  

# items() : 딕셔너리에 있는 키-값 쌍을 얻을 수 있다.
# 딕셔너리의 키-값의 쌍을 매개변수 x에 넣어 x[1][0]. 
# # 즉, AT를 기준으로 오름차순 정렬. 
P = sorted(P.items(), key=lambda x: x[1][1]) 

FT = [0 for i in range(num_process)]     # Finish Time
WT = [0 for i in range(num_process)]     # Waiting Time (TT - BT)
TT = [0 for i in range(num_process)]     # Turnaround Time (FT - AT)
NTT = [0 for i in range(num_process)]    # Normalized TT (TT / BT)

start_time = 0    # 시작시점에 대한 변수
end_time = 0 # 끝난시점에 대한 변수
time = []


for i in range(num_process):
    s_list = [] #start_time이 도착시간보다 작을 때의 리스트
    b_list = [] #start_time이 도착시간보다 클 때의 리스트

    for j in range (num_process):
        if (P[j][1][1] <= start_time) and (P[j][1][3]==0):
            s_list.append(P[j][1])
            
        elif (P[j][1][1] > start_time and P[j][1][3]==0):
            b_list.append(P[j][1])

    
    if len(s_list) != 0: #s_list의 항목이 0이 아닐 때
        s_list.sort(key = lambda x : x[2]) 
        start_time = start_time + s_list[0][2]
        for i in range(num_process): 
            if P[i][1][0] == s_list[0][0]: 
                break
        P[i][1][3] = 1 # 프로세서 스케줄링이 돌아간 것으로 판명하기 위해 마지막 요소를 1로 바꾸어준다.
        end_time = end_time + P[i][1][2] #스케줄링이 끝난시점 = 이전 끝난시점 + burst_time
        time.insert(i, end_time)

    elif len(s_list) == 0 : #s_list가 0일때,
        if start_time <= b_list[0][1]:
            start_time = b_list[0][1]  #start_time에 arrival_time이 제일 작은 값을 더해준다
        start_time = start_time + b_list[0][2] # start_time에 burst_time 값을 더해 다음 스케줄링의 시작값 설정
        
        for i in range(num_process):
            if P[i][1][0] == b_list[0][0]:
                break
        P[i][1][3] = 1
        end_time = end_time + P[i][1][2] #스케줄링이 끝난시점 = 이전 끝난시점 + burst_time
        time.insert(i, end_time)



    ori_AT = []
    for i in range(num_process):
        ori_AT.append(P[i][1][1])

    ori_BT = []
    for i in range(num_process):
        ori_BT.append(P[i][1][2])


for i in range (num_process):
    if P[i][1][3] == 1 :# now[1][2]는 BT
        FT[P[i][1][0]] = time[P[i][1][0]]        # now[1][0]은 idx
        TT[P[i][1][0]] = FT[P[i][1][0]] -  ori_AT[P[i][1][0]]   # now[1][1]은 AT
        WT[P[i][1][0]] = TT[P[i][1][0]] -  ori_BT[P[i][1][0]]
        NTT[P[i][1][0]] = round(TT[P[i][1][0]] / ori_BT[P[i][1][0]], 1)
        

print("\n프로세스 | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Normalized TT |")
total_TT = 0            # TT 다 더한 것
for i in range(num_process):
    total_TT += TT[i]   # for문 돌면서 TT 더하기
    print("   %2s    |      %2s      |     %2s     |      %2s      |        %2s       |       %3s     |"%(P[i][0],P[i][1][1],P[i][1][2], WT[i],TT[i],NTT[i]))
ART = round((total_TT)/num_process, 1)    # ART는 Average Response Time
print("==> Average response time(TT) = {}".format(ART))