# P코어 수정하고 ing 2개 만들기
import queue


class Process:
    def __init__(self, idx, at, bt, numP):
        self.key = "P" + str(idx + 1)
        self.idx = idx
        self.AT = at
        self.BT = bt
        self.OBT = bt  # Original_BT
        self.FT = 0
        self.WT = 0
        self.TT = 0
        self.NTT = 0
        self.tq_flag = 0
        self.core_flag = -1
        self.fast_zero = 0
        self.numP = numP


class Core:
    def __init__(self, pnum, enum):
        self.pnum = pnum  # P코어 개수
        self.enum = enum  # E코어 개수
        self.corenum = pnum + enum  # 총 코어 개수
        self.p_startW = 0.5  # P코어 시동전압
        self.e_startW = 0.1  # E코어 시동전압
        self.pW = 3  # P코어 1초에 3W
        self.eW = 1  # E코어 1초에 1W
        self.totalW = 0  # W 총합
        self.effW = 0  # 소비효율
        self.put_flag = 0
        self.flag = 0
        self.cores = []
        self.kok_flag = [0 for i in range(self.corenum)]
        for i in range(self.corenum):
            self.cores.append(queue.Queue())  # 코어 수만큼 큐 객체 생성

    def allocate_process(self, process):
        self.put_flag = 0  # 프로세스에 넣어준 것 표시
        for i in range(self.corenum):  # 코어 총 개수만큼 반복
            if (self.cores[i].empty() and self.put_flag == 0):  # 큐가 비었다면
                self.cores[i].put(process)  # 큐에 프로세스 넣어줌
                self.put_flag = 1  # 프로세스 넣어준 것 표시
                process.core_flag = i  # 몇번째 코어에 할당됐는지 표시
                if (i < self.pnum):  # 넣은 곳이 P코어라면
                    self.totalW += self.p_startW  # P 시동 전압 더하기
                else:  # 넣은 곳이 E코어라면
                    self.totalW += self.e_startW  # E 시동 전압 더하기
        # for문 끝났는데도 put_flag = 0이라면 아직 못 넣어준 것
        # 그리고 빈 큐가 없었다는 것
        if (self.put_flag == 0):
            # 젤 첫번째 큐에 넣어주기
            self.cores[0].put(process)
            process.core_flag = 0  # 첫번째 코어에 넣어줬다고 표시

    # 지정해서 할당하는 방법
    def fix_allocate_process(self, process):
        self.cores[process.core_flag].put(process)  # core_flag 위치에 넣어줌

    def kok_allocate_process(self, process):
        self.cores[process.idx].put(process)  # 프로세스의 idx 위치에 넣어줌
        self.kok_flag[process.idx] = 1  # 이거 썼다는 표시
        process.core_flag = process.idx  # 몇번째 코어에 할당됐는지 표시

    # 초마다 실행해줘야 함
    def run_core(self):
        result = []
        for i in range(self.corenum):  # 코어 개수만큼 for문 반복
            if (self.cores[i].qsize() > 0):  # 프로세스가 하나라도 있으면
                if (i < self.pnum):  # P코어라면
                    run_p = self.cores[i].get()
                    if (run_p.BT >= 2):  # 프로세스의 BT가 2 이상이면
                        run_p.BT -= 2  # 1초에 BT -2씩
                        result.append(run_p)
                    else:  # BT가 1 이하일 때
                        run_p.BT -= 1
                        result.append(run_p)
                    self.totalW += 3  # 총 전력은 1초에 3W씩 늘어남
                else:  # E코어라면
                    run_e = self.cores[i].get()
                    run_e.BT -= 1  # 1초에 BT -1씩
                    result.append(run_e)
                    self.totalW += 1  # 총 전력은 1초에 1W씩 늘어남
        return result  # 1초에 실행된 프로세스들 (만약 BT가 0이 된 프로세스가 있다면 그 프로세스 처리해)


class RR:
    def __init__(self, process, num_process, tq):

        self.num_process = num_process
        self.tq = tq
        self.P = process
        self.q = queue.Queue()  # 원래 RR 할 때 필요한 큐
        self.time = 0

    def Running(self):
        core = Core(num_pcores, num_ecores)  # 코어 객체 생성
        # AT를 기준으로 오름차순 정렬.
        self.P.sort(key=lambda x: x.AT)

        # 맨 처음에는 self.time인 프로세스를 넣어줌
        for i in range(core.corenum):
            # AT가 self.time 이라면
            if (self.P[i].AT == self.time):
                print()
                self.q.put(self.P[i])

        while (not self.q.empty()):  # 큐가 빌 때까지
            if (core.corenum > self.q.qsize()):  # 코어 수가 큐에 있는 것보다 많거나 같을 때
                for i in range(self.q.qsize()):  # 큐에 있는 만큼 배정
                    now = self.q.get()  # 기존 RR큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if (now.core_flag != -1):
                        core.fix_allocate_process(now)  # 지정해서 할당
                    else:
                        if (now.idx < core.corenum and core.kok_flag[now.idx] == 0):
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)
            else:  # 코어 수가 큐에 있는 것보다 적거나 같을 때
                for i in range(core.corenum):
                    now = self.q.get()  # 기존 RR큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if (now.core_flag != -1):  # 이미 지정되어 있는 애라면
                        core.fix_allocate_process(now)  # 지정된 곳에 할당
                    else:  # 지정되어 있지 않은 애라면
                        if (now.idx < core.corenum and core.kok_flag[now.idx] == 0):
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)
            ###### 여기까지 할당 완료 ###########
            temp = []
            ing = []  # ing   -> BT 0 아니고 tq 안 끝난 거
            ing2 = []  # ing2  -> BT 0 아니고 tq 끝난 거
            allwait = []  # ing 뺀 후에 큐에 있는 거 다 빼기
            arrive = []  # 도착한 애

            # 큐에 남아있는 자식들
            for k in range(self.q.qsize()):
                a = self.q.get()
                allwait.append(a)

            temp = core.run_core()  # 할당한 애들 돌리기
            self.time += 1
            # tq_flag 증가
            for t in range(num_process):
                if (self.P[t].core_flag != -1 and self.P[t].tq_flag < self.tq):  # core에 배정되어 있고 tq_flag가 tq보다 작을 때
                    self.P[t].tq_flag += 1  # tq_flag 증가

            for k in range(len(temp)):  # temp에 기록된 만큼 for문 반복
                print("BT", temp[k].BT)
                if (temp[k].BT == 0):  # 코어 돌리고나서 결과에서 BT가 0이 된 것이 있다면 시간 계산
                    temp[k].FT = self.time
                    print("time", self.time)
                    temp[k].TT = temp[k].FT - temp[k].AT
                    print("FT", temp[k].FT)

                    temp[k].WT = temp[k].TT - temp[k].OBT
                    temp[k].NTT = round(temp[k].TT / temp[k].OBT, 1)
                    temp[k].fast_zero = 1  # fast_zero를 1로

                else:  # BT가 0이 아니라면
                    # 2가지 경우
                    # tq_flag가 안 끝난 경우 (2가지) 안 끝난 경우와 더 빨리 끝난 경우
                    if (temp[k].tq_flag < self.tq):
                        if (temp[k].fast_zero == 0):  # fast_zero가 안 일어난 경우에만 ing에 append
                            ing.append(temp[k])
                    # tq_flag가 끝난 경우
                    elif (temp[k].tq_flag == self.tq):
                        ing2.append(temp[k])
                        # 초기화 작업
                        temp[k].tq_flag = 0  # tq_flag
                        temp[k].core_flag = -1  # core_flag

            # 시간이 증가함에 따라 도착한 프로세스가 있다면
            for j in range(0, self.num_process):
                if (self.P[j].AT == self.time):
                    arrive.append(self.P[j])

            # 큐에 넣기(tq 끝나기 전)
            # ing-allwait-arrive-ing2 순서
            for i in range(len(ing)):
                self.q.put(ing[i])
            for i in range(len(allwait)):
                self.q.put(allwait[i])
            for i in range(len(arrive)):
                self.q.put(arrive[i])
            for i in range(len(ing2)):
                self.q.put(ing2[i])
            temp.clear()
            ing.clear()
            allwait.clear()
            arrive.clear()
            ing2.clear()

    def display(self):
        print("\n프로세스 | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Normalized TT |")
        total_TT = 0  # TT 다 더한 것
        newInfo = []
        for i in range(self.num_process):
            total_TT = total_TT + self.P[i].TT  # for문 돌면서 TT 더하기
            print("   %2s    |      %2s      |     %2s     |      %2s      |        %2s       |       %3s     |" % (
                self.P[i].key, self.P[i].AT, self.P[i].OBT, self.P[i].WT, self.P[i].TT, self.P[i].NTT))
            newInfo.append(self.P[i].WT)
            newInfo.append(self.P[i].TT)
            newInfo.append(self.P[i].NTT)

        ART = round(total_TT / self.num_process, 1)  # ART는 Average Response Time
        print("==> Average response time(TT) = {}".format(ART))
        return newInfo




if __name__ == "__main__":
    print("<RR(Round-Robin)>")
    # num_process = int(input("프로세스의 수를 입력하세요 : "))
    # tq = int(input("자원 사용 제한 시간을 입력하세요 : "))
    # process = [0 for i in range(num_process)]
    # for i in range(num_process):
    #     AT = int(input("P" + str(i + 1) + "의 Arrival time을 입력하세요 : "))
    #     BT = int(input("P" + str(i + 1) + "의 Burst time을 입력하세요 : "))
    #     process[i] = Process(i, AT, BT, num_process)  # 객체 생성
    #
    # num_pcores = int(input("P코어 수를 입력하세요 : "))
    # num_ecores = int(input("E코어 수를 입력하세요 : "))
    #
    # RoundRobin = RR(process, num_process, tq)
    # RoundRobin.Running()
    # RoundRobin.display()

# 프로세스 개수, 타임 퀀텀, [AT, BT], p코어 개수, e코어 개수
def doRR(processNum, timeQuantum, originalInfo, pCoreCnt, eCoreCnt):
    global num_process
    num_process= processNum
    tq = timeQuantum
    process = [0 for i in range(num_process)]
    index = 0
    for i in range(num_process):
        AT = int(originalInfo[index])
        BT = int(originalInfo[index+1])
        process[i] = Process(i, AT, BT, num_process)
        index += 2

    global num_pcores
    num_pcores= pCoreCnt
    global num_ecores
    num_ecores= eCoreCnt

    RoundRobin = RR(process, num_process, tq)
    RoundRobin.Running()
    return RoundRobin.display()


