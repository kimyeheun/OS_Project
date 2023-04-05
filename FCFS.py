print("<FCFS (First-Come-First-Service)>")
P_num = int(input("프로세스의 수를 입력하세요 : "))

P = dict()          # 프로세스 딕셔너리
'''
P = {"P1" : [AT, BT] ...} 이런 형태로 저장
'''
 
for i in range(P_num):
    key = "P"+str(i+1)
    AT = int(input("P"+str(i+1)+"의 Arrival time을 입력하세요 : "))
    BT = int(input("P"+str(i+1)+"의 Burst time을 입력하세요 : "))
    at_bt = []      # at와 bt가 담기는 배열
    at_bt.append(AT)
    at_bt.append(BT)
    P[key] = at_bt
    
# items() : 딕셔너리에 있는 키-값 쌍을 얻을 수 있다.
# 딕셔너리의 키-값의 쌍을 매개변수 x에 넣어 x[1][0]. 
# # 즉, AT를 기준으로 오름차순 정렬. 
P = sorted(P.items(), key=lambda x: x[1][0])
 
FT = []     # FT : Finish Time -> 다 끝내고 나가는 시간
for i in range(len(P)):
    # 첫 번째 프로세스
    if(i==0):
        FT.append(P[i][1][1])
 
    # 전 FT에 그 다음 프로세스의 BT와 더해서 FT에 추가하기
    # ex) P2의 FT는 (P1의 FT) + (P2의 BT)
    else:
        FT.append(FT[i-1] + P[i][1][1])
 
TT = []     # Turnaround Time ( FT - AT )
for i in range(len(P)):
    TT.append(FT[i] - P[i][1][0])
 
WT = []     # Waiting Time ( TT - BT )
for i in range(len(P)):
    WT.append(TT[i] - P[i][1][1])
    
NTT = []    # Normalized TT ( TT/ BT )
for i in range(len(P)):
    # round는 반올림을 위한 함수
    # 소수 첫째자리까지 나오도록 함. 둘째자리에서 반올림.
    NTT.append(round(TT[i] / P[i][1][1], 1))
 
print("\n프로세스 | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Normalized TT |")
for i in range(P_num):
      print("   %2s    |      %2s      |     %2s     |      %2s      |        %2s       |       %3s     |"%(P[i][0],P[i][1][0],P[i][1][1],WT[i],TT[i],NTT[i]))