import queue

print("<RR(Round-Robin)>")
P_num = int(input("프로세스의 수를 입력하세요 : "))
tq = int(input("자원 사용 제한 시간을 입력하세요 : "))      # tq는는 time quantum
P = dict()          # 프로세스 딕셔너리
'''
P = {"P1" : [idx, AT, BT] ...} 이런 형태로 저장
'''
 
for i in range(P_num):
    key = "P"+str(i+1)
    idx = i     # 인덱스 (P1의 인덱스는 0, P2는 1 ...)
    AT = int(input("P"+str(i+1)+"의 Arrival time을 입력하세요 : "))
    BT = int(input("P"+str(i+1)+"의 Burst time을 입력하세요 : "))
    idx_at_bt = []      # idx와 at와 bt가 담기는 배열
    idx_at_bt.append(i)
    idx_at_bt.append(AT)
    idx_at_bt.append(BT)
    P[key] = idx_at_bt
    
# items() : 딕셔너리에 있는 키-값 쌍을 얻을 수 있다.
# 딕셔너리의 키-값의 쌍을 매개변수 x에 넣어 x[1][0]. 
# # 즉, AT를 기준으로 오름차순 정렬. 
P = sorted(P.items(), key=lambda x: x[1][1])

q = queue.Queue()   # 큐 객체 생성
original_BT = []
for i in range(P_num):
    original_BT.append(P[i][1][2])

FT = [0 for i in range(P_num)]     # Finish Time
WT = [0 for i in range(P_num)]     # Waiting Time (TT - BT)
TT = [0 for i in range(P_num)]     # Turnaround Time (FT - AT)
NTT = [0 for i in range(P_num)]    # Normalized TT (TT / BT)
time = 0    # 시간을 위한 변수
# 맨 처음에는 0초인 프로세스를 넣어줌
q.put(P[0])

while(not q.empty()):   # 큐가 빌 때까지
    now = q.get()
    flag = 0            # 끝났는지 판별
    bt = now[1][2]
    for i in range(tq):
        now[1][2] -= 1   # BT 감소
        time += 1           # 1초 증가
        # BT가 0이 되면 나옴
        if(now[1][2] == 0 ):                    # now[1][2]는 BT
            FT[now[1][0]] = time                # now[1][0]은 idx
            TT[now[1][0]] = FT[now[1][0]] - now[1][1]    # now[1][1]은 AT
            WT[now[1][0]] = TT[now[1][0]] - original_BT[now[1][0]]
            NTT[now[1][0]] = round(TT[now[1][0]] / original_BT[now[1][0]], 1)
            flag = 1
            for j in range(0, P_num):
                if(P[j][1][1] == time):     # AT가 time이라면
                    q.put(P[j])             # 큐에 넣어줌
            break
        
        for j in range(0, P_num):
            if(P[j][1][1] == time):     # AT가 time이라면
                q.put(P[j])             # 큐에 넣어줌
                
    # for문이 끝났는데도 BT가 0이 아닌 거라면 다시 큐에 넣어줌
    if(flag == 0):
        q.put(now)
    else : continue
    
print("\n프로세스 | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Normalized TT |")
total_TT = 0            # TT 다 더한 것
for i in range(P_num):
    total_TT += TT[i]   # for문 돌면서 TT 더하기
    print("   %2s    |      %2s      |     %2s     |      %2s      |        %2s       |       %3s     |"%(P[i][0],P[i][1][1],original_BT[i], WT[i],TT[i],NTT[i]))
ART = round((total_TT)/P_num, 1)    # ART는 Average Response Time
print("==> Average response time(TT) = {}".format(ART))