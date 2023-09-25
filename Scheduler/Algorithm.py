import queue


class Process:
    def __init__(self, idx, at, bt, numP):
        self.key = "P" + str(idx + 1)       # 화면 출력에 필요한 key값
        self.idx = idx      # 프로세스의 인덱스 값
        self.AT = at        # Arrival Time
        self.BT = bt        # Burst Time
        self.OBT = bt       # Original Burst Time
        self.FT = 0         # Finish Time
        self.WT = 0         # Waiting Time
        self.TT = 0         # Turnaround Time
        self.NTT = 0        # Normalized Turnaround Time
        self.tq_flag = 0         # 타임 퀀텀 끝났는지 구별을 위한 플래그
        self.core_flag = -1      # 어느 코어에 배정되어 있는지를 보기 위한 플래그
        self.fast_zero = 0       # 타임 퀀텀이 끝나기 전에 BT가 끝난 경우를 위한 플래그
        self.numP = numP         # 프로세스의 수
        self.bt_flag = 0         # HRRN에서 사용
        self.Rratio = 0          # Response Ratio - HRRN에서 사용

    def c_ratio(self):
        self.Rratio = (self.WT + self.OBT) / self.OBT


class Core:
    def __init__(self, pnum, enum):
        self.pnum = pnum                                 # P코어 개수
        self.enum = enum                                 # E코어 개수
        self.corenum = pnum + enum                       # 총 코어 개수
        self.p_startW = 0.5                              # P코어 시동전압
        self.e_startW = 0.1                              # E코어 시동전압
        self.totalW = 0                                  # W 총합
        self.core_totalW = [0, 0, 0, 0]                  # 코어별 W 총합
        self.core_effW = [0, 0, 0, 0]                    # 코어별 소비효율
        self.put_flag = 0                                # 코어에 넣었는지 확인하기 위한 플래그
        self.cores = []                                  # 코어를 담을 배열
        self.kok_flag = [0 for i in range(self.corenum)] # 꼭 넣어야 함을 표시하는 플래그
        for i in range(self.corenum):                    # 코어 수만큼 큐 객체 생성
            self.cores.append(queue.Queue())

    def allocate_process(self, process):
        self.put_flag = 0                                     # 프로세스에 넣어준 것 표시
        for i in range(self.corenum):                         # 코어 총 개수만큼 반복
            if self.cores[i].empty() and self.put_flag == 0:  # 코어가 비었다면
                self.cores[i].put(process)                    # 코어에 프로세스 넣어줌
                self.put_flag = 1                             # 프로세스 넣어준 것 표시
                process.core_flag = i                         # 몇 번째 코어에 할당됐는지 표시
                self.kok_flag[i] = 1

        # for문 끝났는데도 put_flag = 0이라면 아직 못 넣어준 것
        # 그리고 빈 코어가 없었다는 것
        if self.put_flag == 0:
            # 제일 첫 번째 코어에 넣어주기
            self.cores[0].put(process)
            process.core_flag = 0  # 첫 번째 코어에 넣어줬다고 표시

    # 지정해서 할당하는 방법
    def fix_allocate_process(self, process):
        self.cores[process.core_flag].put(process)  # core_flag 위치에 넣어줌

    # 모든 코어 다 쓰기 위해 만든 '꼭' 할당 방법
    def kok_allocate_process(self, process):
        self.cores[process.idx].put(process)  # 프로세스의 idx 위치에 넣어줌
        self.kok_flag[process.idx] = 1        # 이 코어 썼다는 표시
        process.core_flag = process.idx       # 몇번째 코어에 할당됐는지 표시

    # 초마다 실행 해줘야 함
    def run_core(self):
        result = []
        for i in range(self.corenum):      # 코어 개수만큼 for문 반복
            if self.cores[i].qsize() > 0:  # 프로세스가 하나라도 있으면
                if i < self.pnum:          # P코어라면
                    run_p = self.cores[i].get()
                    if run_p.BT >= 2:  # 프로세스의 BT가 2 이상이면
                        run_p.BT -= 2  # 1초에 BT -2씩
                        result.append(run_p)
                    else:  # BT가 1 이하일 때
                        run_p.BT -= 1
                        result.append(run_p)
                else:  # E코어라면
                    run_e = self.cores[i].get()
                    run_e.BT -= 1  # 1초에 BT -1씩
                    result.append(run_e)
        return result  # 1초에 실행된 프로세스들의 상황
        # 만약 BT가 0이 된 프로세스가 있다면 그 프로세스를 처리하도록 함

# todo: FCFS 알고리즘
class FCFS:
    def __init__(self, process, num_process):
        self.num_process = num_process
        self.P = process
        self.q = queue.Queue()  # FCFS 할 때 필요한 큐
        self.time = 0
        self.ready = []
        self.transport = []  # 간트차트에 초마다 전달할 transport
        self.maxFT = 0       # 간트차트에 필요한 maxFT

    def Running(self):
        global core
        core = Core(num_pcores, num_ecores)  # 코어 객체 생성

        # 맨 처음에는 self.time인 프로세스를 넣어줌
        for i in range(self.num_process):
            # AT가 self.time 이라면
            if self.P[i].AT == self.time:
                self.ready.append(self.P[i])  # ready 리스트 안에 값 넣기

        for i in range(len(self.ready)):
            self.q.put(self.ready[i])

        while not self.endSimulation() or not self.q.empty():  # 큐가 빌 때까지
            if core.corenum > self.q.qsize():    # 코어 수가 큐에 있는 것보다 많거나 같을 때
                for i in range(self.q.qsize()):  # 큐에 있는 만큼 배정
                    # 기존 FCFS큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    now = self.q.get()
                    if now.core_flag != -1:
                        core.fix_allocate_process(now)  # 지정해서 할당
                    else:
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            else:  # 코어 수가 큐에 있는 것보다 적거나 같을 때
                for i in range(core.corenum):
                    now = self.q.get()                  # 기존 FCFS 큐는 계속 있음.
                                                        # 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if (now.core_flag != -1):           # 이미 지정되어 있는 애라면
                        core.fix_allocate_process(now)  # 지정된 곳에 할당

                    else:  # 지정되어 있지 않은 애라면
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            # ##### 여기까지 할당 완료 ###########
            temp = []
            ing = []  # 실행중인 애(아직 끝나지 X)
            allwait = []

            # 큐에 남아있는 자식들
            for k in range(self.q.qsize()):
                a = self.q.get()  # 꺼내서
                allwait.append(a)  # allwait에 append시키고

            temp = core.run_core()  # 할당한 애들 돌리기

            # 간트 차트를 위해
            # 형태를 [[0,0,0,0], [0,0,0,0], [0,0,0,0],...]
            trans = [0, 0, 0, 0]
            for k in range(core.corenum):
                for i in range(num_process):
                    # P[i] 프로세스가 할당된 코어가 k라면
                    if k == self.P[i].core_flag:
                        trans[k] = i + 1    # 0, 1, 2, 3으로 표시했기에 전달할 때는 + 1
                        break
            self.transport.append(trans)  # 최종적으로 전달할 배열인 self.transport에 trans 추가
            self.maxFT += 1     # 맨 마지막으로 끝나는 시간

            self.time += 1
            for k in range(len(temp)):  # temp에 기록된 만큼 for문 반복
                if temp[k].BT == 0:     # 코어 돌리고나서 결과에서 BT가 0이 된 것이 있다면 시간 계산
                    temp[k].FT = self.time
                    temp[k].TT = temp[k].FT - temp[k].AT
                    temp[k].WT = temp[k].TT - temp[k].OBT
                    temp[k].NTT = round(temp[k].TT / temp[k].OBT, 1)
                    temp[k].core_flag = -1  # core_flag 초기화
                else:  # BT가 0이 아니라면
                    ing.append(temp[k])

            # 시간이 증가함에 따라 도착한 프로세스가 있다면
            for j in range(0, self.num_process):
                if self.P[j].AT == self.time:
                    allwait.append(self.P[j])

            # 큐에 넣기
            for i in range(len(ing)):
                self.q.put(ing[i])
            for i in range(len(allwait)):
                self.q.put(allwait[i])

            temp.clear()
            ing.clear()
            allwait.clear()

    # BT가 0이 아닌게 있으면 False / 다 끝났으면 True
    def endSimulation(self):
        sumBt = 0
        for i in range(self.num_process):
            sumBt += self.P[i].BT
        if sumBt == 0:
            return True
        return False

    def display(self):
        # 시동 전력 구하기
        for k in range(core.corenum):
            if k < core.pnum:  # P코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 3
                        core.core_totalW[k] += 3
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.p_startW
                            core.core_totalW[k] += core.p_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:  # 첫번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.p_startW
                        core.core_totalW[k] += core.p_startW
            else:  # E코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 1
                        core.core_totalW[k] += 1
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.e_startW
                            core.core_totalW[k] += core.e_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:
                        # 첫 번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.e_startW
                        core.core_totalW[k] += core.e_startW

        coreW = []
        # 코어 별 소비효율 = 코어 별 총 소비전력 / 총 소비 전력
        for i in range(core.corenum):
            coreW.append(round(core.core_totalW[i], 1))

        corePercent = []
        for i in range(core.corenum):
            core.core_effW[i] = round((core.core_totalW[i] / core.totalW) * 100, 1)
            corePercent.append(core.core_effW[i])

        newInfo = []
        for i in range(self.num_process):
            newInfo.append(self.P[i].WT if self.P[i].WT > 0 else 0)
            newInfo.append(self.P[i].TT)
            newInfo.append(self.P[i].NTT)

        resultInfo = {"newInfo": newInfo,
                      "transport": self.transport,
                      "maxFT": self.maxFT,
                      "coreW": coreW,
                      "corePercent": corePercent}
        return resultInfo


# todo : RR 알고리즘
class RR:
    def __init__(self, process, num_process, tq):
        self.num_process = num_process   # 프로세스의 개수
        self.tq = tq                     # 타임 퀀텀
        self.P = process                 # 입력된 프로세스들이 담겨있는 배열
        self.q = queue.Queue()           # 큐 객체 생성
        self.time = 0                    # 시간
        self.transport = []              # 간트차트에 초마다 전달할 transport
        self.maxFT = 0                   # 간트차트에 필요한 maxFT

    def Running(self):
        global core
        core = Core(num_pcores, num_ecores)  # 코어 객체 생성

        # AT를 기준으로 오름차순 정렬.
        self.P.sort(key=lambda object: object.AT)

        for i in range(num_process):
            # AT가 self.time 이라면
            if self.P[i].AT == self.time:
                self.q.put(self.P[i])

        while not self.endSimulation() or not self.q.empty():  # 큐가 빌 때까지
            if core.corenum > self.q.qsize():  # 코어 수가 큐에 있는 것보다 많거나 같을 때
                for i in range(self.q.qsize()):  # 큐에 있는 만큼 배정
                    # 기존 RR큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정 해주는 것.
                    now = self.q.get()
                    if now.core_flag != -1:
                        core.fix_allocate_process(now)  # 지정해서 할당
                    else:
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)
            else:  # 코어 수가 큐에 있는 것보다 적거나 같을 때
                for i in range(core.corenum):
                    now = self.q.get()  # 기존 RR큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if now.core_flag != -1:  # 이미 지정되어 있는 애라면
                        core.fix_allocate_process(now)  # 지정된 곳에 할당
                    else:  # 지정되어 있지 않은 애라면
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            # ##### 여기까지 할당 완료 ###########
            temp = []     # 코어 실행하고 반환 받은 값을 저장할 temp 배열
            ing = []      # ing   -> BT 0 아니고 tq 안 끝난 거
            ing2 = []     # ing2  -> BT 0 아니고 tq 끝난 거
            allwait = []  # ing 뺀 후에 큐에 있는 거 다 빼기
            arrive = []   # 도착한 프로세스를 넣을 배열

            # 큐에 남아있는 프로세스들
            for k in range(self.q.qsize()):
                a = self.q.get()          # 큐에서 빼고
                allwait.append(a)         # allwait에 append

            temp = core.run_core()        # 코어 실행

            # 끝나는 시간
            # 몇 차원 배열인지는 코어 개수로 판단
            # 난 형태를 [[0,0,0,0], [0,0,0,0], [0,0,0,0]]
            trans = [0, 0, 0, 0]
            for k in range(core.corenum):
                for i in range(num_process):
                    # Pi 프로세스가 할당된 코어가 k라면
                    if k == self.P[i].core_flag:
                        trans[k] = i + 1
                        break
            self.transport.append(trans)  # 최종적으로 전달할 배열인 self.transport에 trans 추가
            self.maxFT += 1

            self.time += 1
            # tq_flag 증가
            for t in range(num_process):
                # core에 배정되어 있고 tq_flag가 tq보다 작을 때
                if self.P[t].core_flag != -1 and self.P[t].tq_flag < self.tq:
                    self.P[t].tq_flag += 1  # tq_flag 증가

            for k in range(len(temp)):  # temp에 기록된 만큼 for문 반복
                # 코어 돌리고나서 결과에서 BT가 0이 된 것이 있다면 시간 계산
                if temp[k].BT == 0:
                    temp[k].FT = self.time
                    temp[k].TT = temp[k].FT - temp[k].AT
                    temp[k].WT = temp[k].TT - temp[k].OBT
                    temp[k].NTT = round(temp[k].TT / temp[k].OBT, 1)
                    temp[k].fast_zero = 1  # fast_zero를 1로
                    temp[k].core_flag = -1  # core_flag를 -1로 초기화

                else:  # BT가 0이 아니라면
                    # 2가지 경우가 있음
                    #### 1. tq_flag가 안 끝난 경우 ####
                    if temp[k].tq_flag < self.tq:
                        if temp[k].fast_zero == 0:  # fast_zero가 안 일어난 경우에만 ing에 append
                            ing.append(temp[k])
                    #### 2. tq_flag가 끝난 경우 ####
                    elif temp[k].tq_flag == self.tq:
                        ing2.append(temp[k])
                        # 초기화 작업
                        temp[k].tq_flag = 0
                        temp[k].core_flag = -1

            # 시간이 증가함에 따라 도착한 프로세스가 있다면
            for j in range(0, self.num_process):
                if self.P[j].AT == self.time:
                    arrive.append(self.P[j])

            # 큐에 넣기
            # ing-allwait-arrive-ing2 순서
            for i in range(len(ing)):
                self.q.put(ing[i])
            for i in range(len(allwait)):
                self.q.put(allwait[i])
            for i in range(len(arrive)):
                self.q.put(arrive[i])
            for i in range(len(ing2)):
                self.q.put(ing2[i])

            # 배열 초기화
            temp.clear()
            ing.clear()
            allwait.clear()
            arrive.clear()
            ing2.clear()

    def endSimulation(self):
        sumBt = 0
        for i in range(self.num_process):
            sumBt += self.P[i].BT
        if sumBt == 0:
            return True
        return False

    def display(self):
        # 시동 전력 구하기
        for k in range(core.corenum):
            if k < core.pnum:  # P코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 3
                        core.core_totalW[k] += 3
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.p_startW
                            core.core_totalW[k] += core.p_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:  # 첫번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.p_startW
                        core.core_totalW[k] += core.p_startW
            else:  # E코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 1
                        core.core_totalW[k] += 1
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.e_startW
                            core.core_totalW[k] += core.e_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:
                        # 첫 번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.e_startW
                        core.core_totalW[k] += core.e_startW

        coreW = []
        # 코어 별 소비효율 = 코어 별 총 소비전력 / 총 소비 전력
        for i in range(core.corenum):
            coreW.append(round(core.core_totalW[i], 1))

        corePercent = []
        for i in range(core.corenum):
            core.core_effW[i] = round((core.core_totalW[i] / core.totalW) * 100, 1)
            corePercent.append(core.core_effW[i])

        newInfo = []
        for i in range(self.num_process):
            newInfo.append(self.P[i].WT if self.P[i].WT > 0 else 0)
            newInfo.append(self.P[i].TT)
            newInfo.append(self.P[i].NTT)

        resultInfo = {"newInfo": newInfo,
                      "transport": self.transport,
                      "maxFT": self.maxFT,
                      "coreW": coreW,
                      "corePercent": corePercent}
        return resultInfo


# todo : SPN 알고리즘
class SPN:
    def __init__(self, process, num_process):
        self.num_process = num_process
        self.P = process
        self.q = queue.Queue()  # SPN 할 때 필요한 큐
        self.time = 0
        self.ready = []
        self.transport = []     # 간트차트에 초마다 전달할 transport
        self.maxFT = 0          # 간트차트에 필요한 maxFT

    def Running(self):
        global core
        core = Core(num_pcores, num_ecores)  # 코어 객체 생성

        # 맨 처음에는 self.time인 프로세스를 넣어줌
        for i in range(self.num_process):
            # AT가 self.time 이라면
            if self.P[i].AT == self.time:
                self.ready.append(self.P[i])  # ready 리스트 안에 값 넣기
        self.ready.sort(key=lambda x: x.BT)

        for i in range(len(self.ready)):
            self.q.put(self.ready[i])

        while not self.endSimulation() or not self.q.empty():  # 큐가 빌 때까지
            if core.corenum > self.q.qsize():  # 코어 수가 큐에 있는 것보다 많거나 같을 때
                for i in range(self.q.qsize()):  # 큐에 있는 만큼 배정
                    # 기존 SPN큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    now = self.q.get()
                    if now.core_flag != -1:
                        core.fix_allocate_process(now)  # 지정해서 할당
                    else:
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            else:  # 코어 수가 큐에 있는 것보다 적거나 같을 때
                for i in range(core.corenum):
                    now = self.q.get()  # 기존 SPN큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if now.core_flag != -1:  # 이미 지정되어 있는 애라면
                        core.fix_allocate_process(now)  # 지정된 곳에 할당

                    else:  # 지정되어 있지 않은 애라면
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            # ##### 여기까지 할당 완료 ###########
            temp = []     # 동작을 수행하기 위한 프로세스가 담긴 리스트
            ing = []      # 동작 수행 후에도 계속 동작을 진행하는 프로세스가 담긴 리스트
            allwait = []  # 동작을 위한 차례를 기다리는 프로세스가 담긴 리스트

            # 큐에 남아있는 자식들
            for k in range(self.q.qsize()):
                a = self.q.get()  # 꺼내서
                allwait.append(a)  # allwait에 append시키고
                allwait.sort(key=lambda x: x.BT)  # BT로 정렬하기

            temp = core.run_core()  # 할당한 애들 돌리기

            # 끝나는 시간
            # 몇 차원 배열인지는 코어 개수로 판단
            # 난 형태를 [[0,0,0,0], [0,0,0,0], [0,0,0,0]]
            trans = [0, 0, 0, 0]
            for k in range(core.corenum):
                for i in range(num_process):
                    # Pi 프로세스가 할당된 코어가 k라면
                    if (k == self.P[i].core_flag):
                        trans[k] = i + 1
                        break
            self.transport.append(trans)  # 최종적으로 전달할 배열인 self.transport에 trans 추가
            self.maxFT += 1

            self.time += 1
            for k in range(len(temp)):  # temp에 기록된 만큼 for문 반복
                if temp[k].BT == 0:     # 코어 돌리고나서 결과에서 BT가 0이 된 것이 있다면 시간 계산
                    temp[k].FT = self.time
                    temp[k].TT = temp[k].FT - temp[k].AT
                    temp[k].WT = temp[k].TT - temp[k].OBT
                    temp[k].NTT = round(temp[k].TT / temp[k].OBT, 1)
                    temp[k].core_flag = -1  # core_flag 초기화
                else:  # BT가 0이 아니라면
                    ing.append(temp[k])

            # 시간이 증가함에 따라 도착한 프로세스가 있다면
            for j in range(0, self.num_process):
                if self.P[j].AT == self.time:
                    allwait.append(self.P[j])
                    allwait.sort(key=lambda x: x.BT)

            # 큐에 넣기
            for i in range(len(ing)):
                self.q.put(ing[i])
            for i in range(len(allwait)):
                self.q.put(allwait[i])

            temp.clear()
            ing.clear()
            allwait.clear()

    def endSimulation(self):
        sumBt = 0
        for i in range(self.num_process):
            sumBt += self.P[i].BT
        if sumBt == 0:
            return True
        return False

    def display(self):
        # 시동 전력 구하기
        for k in range(core.corenum):
            if k < core.pnum:  # P코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 3
                        core.core_totalW[k] += 3
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.p_startW
                            core.core_totalW[k] += core.p_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:  # 첫번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.p_startW
                        core.core_totalW[k] += core.p_startW
            else:  # E코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 1
                        core.core_totalW[k] += 1
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.e_startW
                            core.core_totalW[k] += core.e_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:
                        # 첫 번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.e_startW
                        core.core_totalW[k] += core.e_startW

        coreW = []
        # 코어 별 소비효율 = 코어 별 총 소비전력 / 총 소비 전력
        for i in range(core.corenum):
            coreW.append(round(core.core_totalW[i], 1))

        corePercent = []
        for i in range(core.corenum):
            core.core_effW[i] = round((core.core_totalW[i] / core.totalW) * 100, 1)
            corePercent.append(core.core_effW[i])

        newInfo = []
        for i in range(self.num_process):
            newInfo.append(self.P[i].WT if self.P[i].WT > 0 else 0)
            newInfo.append(self.P[i].TT)
            newInfo.append(self.P[i].NTT)

        resultInfo = {"newInfo": newInfo,
                      "transport": self.transport,
                      "maxFT": self.maxFT,
                      "coreW": coreW,
                      "corePercent": corePercent}
        return resultInfo


# todo : SRTN 알고리즘
class SRTN:
    def __init__(self, process, num_process):
        self.num_process = num_process
        self.P = process
        self.q = queue.Queue()  # 원래 RR 할 때 필요한 큐
        self.ready = []
        self.time = 0
        self.arr_flag = 0
        self.transport = []     # 간트차트에 초마다 전달할 transport
        self.maxFT = 0          # 간트차트에 필요한 maxFT

    def Running(self):
        global core
        core = Core(num_pcores, num_ecores)   # 코어 객체 생성

        # 맨 처음에는 self.time인 프로세스를 넣어줌
        for i in range(self.num_process):
            # AT가 self.time 이라면
            if self.P[i].AT == self.time:
                self.ready.append(self.P[i])  # ready 리스트 안에 값 넣기
        self.ready.sort(key=lambda x: x.BT)   # ready 리스트를 BT값을 기준으로 정렬

        for i in range(len(self.ready)):      # ready값을 q에 넣기
            self.q.put(self.ready[i])

        while not self.q.empty() or not self.endSimulation():  # 큐가 빌 때까지
            if core.corenum > self.q.qsize():  # 코어 수가 큐에 있는 것보다 많거나 같을 때
                for i in range(self.q.qsize()):  # 큐에 있는 만큼 배정
                    now = self.q.get()  # 기존 SPN큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if now.core_flag != -1:
                        core.fix_allocate_process(now)  # 지정해서 할당
                    else:
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            else:  # 코어 수가 큐에 있는 것보다 적거나 같을 때
                for i in range(core.corenum):
                    now = self.q.get()  # 기존 SPN큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if now.core_flag != -1:  # 이미 지정되어 있는 애라면
                        core.fix_allocate_process(now)  # 지정된 곳에 할당

                    else:  # 지정되어 있지 않은 애라면
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서

            # ####### 여기까지 할당 완료 ###########
            temp = []  # 1초 실행 후 결과
            ing = []  # ing   -> BT가 0이 아니고, 가장 작은 BT라 현재 돌아가고 있는 것
            allwait = []  # ing 뺀 후에 큐에 있는 거 다 빼기
            arrive = []  # 도착한 프로세스 있는 경우
            qready = []

            # 큐에 남아있는 자식들을 allwait에 넣고 BT 정렬
            for k in range(self.q.qsize()):
                a = self.q.get()  # 꺼내서
                allwait.append(a)  # allwait에 append시키고

            temp = core.run_core()  # 할당한 애들 돌리기
            # 형태를 [[0,0,0,0], [0,0,0,0], [0,0,0,0]]
            trans = [0, 0, 0, 0]
            for k in range(core.corenum):
                for i in range(num_process):
                    # Pi 프로세스가 할당된 코어가 k라면
                    if (k == self.P[i].core_flag):
                        trans[k] = i + 1
                        break
            self.transport.append(trans)  # 최종적으로 전달할 배열인 self.transport에 trans 추가
            self.maxFT += 1

            self.time += 1
            # 시간이 증가함에 따라 도착한 프로세스가 있다면
            for j in range(self.num_process):
                if (self.P[j].AT == self.time):
                    arrive.append(self.P[j])
                    # 코어 플래그 다 초기화
                    for c in range(num_process):
                        self.P[c].core_flag = -1


            for k in range(len(temp)):      # temp에 기록된 만큼 for문 반복
                if (temp[k].BT == 0):       # BT가 0이 된 것이 있다면 시간 계산
                    temp[k].FT = self.time
                    temp[k].TT = temp[k].FT - temp[k].AT
                    temp[k].WT = temp[k].TT - temp[k].OBT
                    temp[k].NTT = round(temp[k].TT / temp[k].OBT, 1)
                    temp[k].core_flag = -1  # core_flag 초기화

                else:  # BT가 0이 아니라면
                    ing.append(temp[k])

            qready = ing + arrive + allwait
            qready.sort(key=lambda x: x.BT)  # BT 순으로 정렬

            for q in range(len(qready)):
                self.q.put(qready[q])

            temp.clear()
            ing.clear()
            allwait.clear()
            arrive.clear()
            qready.clear()

    def endSimulation(self):
        sumBt = 0
        for i in range(self.num_process):
            sumBt += self.P[i].BT
        if sumBt == 0:
            return True
        return False

    def display(self):
        # 시동 전력 구하기
        for k in range(core.corenum):
            if k < core.pnum:  # P코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 3
                        core.core_totalW[k] += 3
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.p_startW
                            core.core_totalW[k] += core.p_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:  # 첫번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.p_startW
                        core.core_totalW[k] += core.p_startW
            else:  # E코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 1
                        core.core_totalW[k] += 1
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.e_startW
                            core.core_totalW[k] += core.e_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:
                        # 첫 번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.e_startW
                        core.core_totalW[k] += core.e_startW

        coreW = []
        # 코어 별 소비효율 = 코어 별 총 소비전력 / 총 소비 전력
        for i in range(core.corenum):
            coreW.append(round(core.core_totalW[i], 1))

        corePercent = []
        for i in range(core.corenum):
            core.core_effW[i] = round((core.core_totalW[i] / core.totalW) * 100, 1)
            corePercent.append(core.core_effW[i])

        newInfo = []
        for i in range(self.num_process):
            newInfo.append(self.P[i].WT if self.P[i].WT > 0 else 0)
            newInfo.append(self.P[i].TT)
            newInfo.append(self.P[i].NTT)

        resultInfo = {"newInfo": newInfo,
                      "transport": self.transport,
                      "maxFT": self.maxFT,
                      "coreW": coreW,
                      "corePercent": corePercent}
        return resultInfo


# todo : HRRN 알고리즘
class HRRN:
    def __init__(self, process, num_process):
        self.num_process = num_process
        self.P = process
        self.q = queue.Queue()  # HRRN 할 때 필요한 큐
        self.time = 0
        self.ready = []
        self.transport = []     # 간트차트에 초마다 전달할 transport
        self.maxFT = 0          # 간트차트에 필요한 maxFT
        self.bt_flag = 0

    def Running(self):
        global core
        core = Core(num_pcores, num_ecores)  # 코어 객체 생성

        # 맨 처음에는 self.time인 프로세스를 넣어줌
        for i in range(self.num_process):
            # AT가 self.time 이라면
            if self.P[i].AT == self.time:
                self.ready.append(self.P[i])  # ready 리스트 안에 값 넣기

        for i in range(len(self.ready)):
            self.q.put(self.ready[i])

        while not self.endSimulation() or not self.q.empty():  # 큐가 빌 때까지
            if core.corenum > self.q.qsize():  # 코어 수가 큐에 있는 것보다 많거나 같을 때
                for i in range(self.q.qsize()):  # 큐에 있는 만큼 배정
                    now = self.q.get()  # 기존 HRRN큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if now.core_flag != -1:
                        core.fix_allocate_process(now)  # 지정해서 할당
                    else:
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            else:  # 코어 수가 큐에 있는 것보다 적거나 같을 때
                for i in range(core.corenum):
                    now = self.q.get()  # 기존 HRRN큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if now.core_flag != -1:  # 이미 지정되어 있는 애라면
                        core.fix_allocate_process(now)  # 지정된 곳에 할당

                    else:  # 지정되어 있지 않은 애라면
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            # ##### 여기까지 할당 완료 ###########
            temp = []     # 동작을 수행하기 위한 프로세스가 담긴 리스트
            ing = []      # 동작 수행 후에도 계속 동작을 진행하는 프로세스가 담긴 리스트
            allwait = []  # 동작을 위한 차례를 기다리는 프로세스가 담긴 리스트

            # 큐에 남아있는 프로세스들
            for k in range(self.q.qsize()):
                a = self.q.get()    # 꺼내서
                allwait.append(a)   # allwait에 append시키고

            temp = core.run_core()  # 할당한 프로세스 동작하기

            # 끝나는 시간
            # 몇 차원 배열인지는 코어 개수로 판단
            # 난 형태를 [[0,0,0,0], [0,0,0,0], [0,0,0,0]]
            trans = [0, 0, 0, 0]
            for k in range(core.corenum):
                for i in range(num_process):
                    # Pi 프로세스가 할당된 코어가 k라면
                    if k == self.P[i].core_flag:
                        trans[k] = i + 1
                        break
            self.transport.append(trans)  # 최종적으로 전달할 배열인 self.transport에 trans 추가
            self.maxFT += 1

            self.time += 1
            for k in range(len(temp)):  # temp에 기록된 만큼 for문 반복
                if temp[k].BT == 0:  # 코어 돌리고나서 결과에서 BT가 0이
                    # 된 것이 있다면 시간 계산
                    temp[k].FT = self.time
                    temp[k].TT = temp[k].FT - temp[k].AT
                    temp[k].WT = temp[k].TT - temp[k].OBT
                    temp[k].NTT = round(temp[k].TT / temp[k].OBT, 1)
                    temp[k].core_flag = -1  # core_flag 초기화
                    self.bt_flag = 1

                else:  # BT가 0이 아니라면
                    ing.append(temp[k])

            # 시간이 증가함에 따라 도착한 프로세스가 있다면
            for j in range(0, self.num_process):
                if self.P[j].AT == self.time:
                    allwait.append(self.P[j])

            if self.bt_flag == 1:
                for i in range(len(allwait)):
                    allwait[i].FT = self.time
                    allwait[i].TT = allwait[i].FT - allwait[i].AT
                    allwait[i].WT = allwait[i].TT - allwait[i].OBT
                    allwait[i].Rratio = (allwait[i].OBT + allwait[i].WT) / allwait[i].OBT
                allwait.sort(key=lambda x: -x.Rratio)  # ratio로 정렬하기
                self.bt_flag = 0

                # 큐에 넣기
            for i in range(len(ing)):
                self.q.put(ing[i])
            for i in range(len(allwait)):
                self.q.put(allwait[i])

            temp.clear()
            ing.clear()
            allwait.clear()

    def endSimulation(self):
        sumBt = 0
        for i in range(self.num_process):
            sumBt += self.P[i].BT
        if sumBt == 0:
            return True
        return False

    def display(self):
        # 시동 전력 구하기
        for k in range(core.corenum):
            if k < core.pnum:  # P코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 3
                        core.core_totalW[k] += 3
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.p_startW
                            core.core_totalW[k] += core.p_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:  # 첫번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.p_startW
                        core.core_totalW[k] += core.p_startW
            else:  # E코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 1
                        core.core_totalW[k] += 1
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.e_startW
                            core.core_totalW[k] += core.e_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:
                        # 첫 번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.e_startW
                        core.core_totalW[k] += core.e_startW

        coreW = []
        # 코어 별 소비효율 = 코어 별 총 소비전력 / 총 소비 전력
        for i in range(core.corenum):
            coreW.append(round(core.core_totalW[i], 1))

        corePercent = []
        for i in range(core.corenum):
            core.core_effW[i] = round((core.core_totalW[i] / core.totalW) * 100, 1)
            corePercent.append(core.core_effW[i])

        newInfo = []
        for i in range(self.num_process):
            newInfo.append(self.P[i].WT if self.P[i].WT > 0 else 0)
            newInfo.append(self.P[i].TT)
            newInfo.append(self.P[i].NTT)

        resultInfo = {"newInfo": newInfo,
                      "transport": self.transport,
                      "maxFT": self.maxFT,
                      "coreW": coreW,
                      "corePercent": corePercent}
        return resultInfo


# todo : BOSS 알고리즘
class BOSS:
    def __init__(self, process, num_process):
        self.num_process = num_process
        self.P = process
        self.q = queue.Queue()  # 필요한 큐
        self.ready = []
        self.time = 0
        self.arr_flag = 0
        self.transport = []  # 간트차트에 초마다 전달할 transport
        self.maxFT = 0  # 간트차트에 필요한 maxFT

    def Running(self):
        global core
        core = Core(num_pcores, num_ecores)  # 코어 객체 생성

        # 맨 처음에는 self.time인 프로세스를 넣어줌
        for i in range(self.num_process):
            # AT가 self.time 이라면
            if (self.P[i].AT == self.time):
                self.ready.append(self.P[i])  # ready 리스트 안에 값 넣기
        self.ready.sort(key=lambda x: -x.BT)  # ready 리스트를 BT값을 기준으로 내림차순 정렬

        for i in range(len(self.ready)):  # ready값을 q에 넣기
            self.q.put(self.ready[i])

        while not self.q.empty() or not self.endSimulation():  # 큐가 빌 때까지
            if core.corenum > self.q.qsize():  # 코어 수가 큐에 있는 것보다 많거나 같을 때
                for i in range(self.q.qsize()):  # 큐에 있는 만큼 배정
                    now = self.q.get()  # 기존 큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if now.core_flag != -1:
                        core.fix_allocate_process(now)  # 지정해서 할당
                    else:
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            else:  # 코어 수가 큐에 있는 것보다 적거나 같을 때
                for i in range(core.corenum):
                    now = self.q.get()  # 기존 큐는 계속 있음. 여기에 있는 것을 꺼낼 때마다 코어에 배정해주는 것.
                    if now.core_flag != -1:  # 이미 지정되어 있는 애라면
                        core.fix_allocate_process(now)  # 지정된 곳에 할당

                    else:  # 지정되어 있지 않은 애라면
                        if now.idx < core.corenum and core.kok_flag[now.idx] == 0:
                            core.kok_allocate_process(now)
                        else:
                            core.allocate_process(now)  # 기존 방식(빈 곳 찾아서)

            # ####### 여기까지 할당 완료 ###########
            temp = []      # 1초 실행 후 결과
            ing = []       # ing -> BT가 0이 아니고, 가장 작은 BT라 현재 돌아가고 있는 것
            allwait = []   # ing 뺀 후에 큐에 있는 거 다 빼기
            arrive = []    # 도착한 프로세스 있는 경우
            qready = []

            # 큐에 남아있는 자식들을 allwait에 넣기
            for k in range(self.q.qsize()):
                a = self.q.get()    # 꺼내서
                allwait.append(a)   # allwait에 append시키고

            # allwait정렬??

            temp = core.run_core()  # 할당한 애들 돌리기

            # 형태를 [[0,0,0,0], [0,0,0,0], [0,0,0,0]]
            trans = [0, 0, 0, 0]
            for k in range(core.corenum):
                for i in range(num_process):
                    # Pi 프로세스가 할당된 코어가 k라면
                    if k == self.P[i].core_flag:
                        trans[k] = i + 1
                        break
            self.transport.append(trans)  # 최종적으로 전달할 배열인 self.transport에 trans 추가
            self.maxFT += 1

            self.time += 1
            # 시간이 증가함에 따라 도착한 프로세스가 있다면
            for j in range(self.num_process):
                if self.P[j].AT == self.time:
                    arrive.append(self.P[j])
                    # 코어 플래그 다 초기화
                for c in range(num_process):
                    self.P[c].core_flag = -1

            for k in range(len(temp)):      # temp에 기록된 만큼 for문 반복
                if temp[k].BT == 0:         # BT가 0이 된 것이 있다면 시간 계산
                    temp[k].FT = self.time
                    temp[k].TT = temp[k].FT - temp[k].AT
                    temp[k].WT = temp[k].TT - temp[k].OBT
                    temp[k].NTT = round(temp[k].TT / temp[k].OBT, 1)
                    temp[k].core_flag = -1  # core_flag 초기화

                else:  # BT가 0이 아니라면
                    ing.append(temp[k])

            qready = ing + arrive + allwait
            qready.sort(key=lambda x: -x.BT)  # BT 순으로 내림차순 정렬

            for q in range(len(qready)):
                self.q.put(qready[q])

            temp.clear()
            ing.clear()
            allwait.clear()
            arrive.clear()
            qready.clear()

    def endSimulation(self):
        sumBt = 0
        for i in range(self.num_process):
            sumBt += self.P[i].BT
        if sumBt == 0:
            return True
        return False

    def display(self):
        # 시동 전력 구하기
        for k in range(core.corenum):
            if k < core.pnum:  # P코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 3
                        core.core_totalW[k] += 3
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.p_startW
                            core.core_totalW[k] += core.p_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:  # 첫번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.p_startW
                        core.core_totalW[k] += core.p_startW
            else:  # E코어라면
                for i in range(len(self.transport)):
                    if self.transport[i][k] != 0:
                        core.totalW += 1
                        core.core_totalW[k] += 1
                    if i - 1 >= 0:
                        if self.transport[i - 1][k] == 0 and self.transport[i][k] != 0:
                            # 이전 값이 0이고 현재 값이 0이 아니라면 시동전력 더하기
                            core.totalW += core.e_startW
                            core.core_totalW[k] += core.e_startW
                    elif i - 1 < 0 and self.transport[i][k] != 0:
                        # 첫 번째 배열이고 지금 값이 0이 아니라면 시동전력 더하기
                        core.totalW += core.e_startW
                        core.core_totalW[k] += core.e_startW

        coreW = []
        # 코어 별 소비효율 = 코어 별 총 소비전력 / 총 소비 전력
        for i in range(core.corenum):
            coreW.append(round(core.core_totalW[i], 1))

        corePercent = []
        for i in range(core.corenum):
            core.core_effW[i] = round((core.core_totalW[i] / core.totalW) * 100, 1)
            corePercent.append(core.core_effW[i])

        newInfo = []
        for i in range(self.num_process):
            newInfo.append(self.P[i].WT if self.P[i].WT > 0 else 0)
            newInfo.append(self.P[i].TT)
            newInfo.append(self.P[i].NTT)

        resultInfo = {"newInfo": newInfo,
                      "transport": self.transport,
                      "maxFT": self.maxFT,
                      "coreW": coreW,
                      "corePercent": corePercent}
        return resultInfo


# 프로세스 개수, 타임 퀀텀, [AT, BT], p코어 개수, e코어 개수
# todo : doFCFS
def doFCFS(processNum, originalInfo, pCoreCnt, eCoreCnt):
    global num_process
    num_process = processNum
    process = [0 for i in range(num_process)]
    index = 0
    for i in range(num_process):
        AT = int(originalInfo[index])
        BT = int(originalInfo[index + 1])
        process[i] = Process(i, AT, BT, num_process)
        index += 2

    global num_pcores
    num_pcores = pCoreCnt
    global num_ecores
    num_ecores = eCoreCnt

    FistComeFirstService = FCFS(process, num_process)
    FistComeFirstService.Running()
    resultInfo = FistComeFirstService.display()
    return resultInfo


# 프로세스 개수, 타임 퀀텀, [AT, BT], p코어 개수, e코어 개수
# todo : doRR
def doRR(processNum, timeQuantum, originalInfo, pCoreCnt, eCoreCnt):
    global num_process
    num_process = processNum
    tq = timeQuantum
    process = [0 for i in range(num_process)]
    index = 0
    for i in range(num_process):
        AT = int(originalInfo[index])
        BT = int(originalInfo[index + 1])
        process[i] = Process(i, AT, BT, num_process)
        index += 2

    global num_pcores
    num_pcores = pCoreCnt
    global num_ecores
    num_ecores = eCoreCnt

    RoundRobin = RR(process, num_process, tq)
    RoundRobin.Running()
    resultInfo = RoundRobin.display()
    return resultInfo


# todo : doSPN
def doSPN(processNum, originalInfo, pCoreCnt, eCoreCnt):
    global num_process
    num_process = processNum
    process = [0 for i in range(num_process)]
    index = 0
    for i in range(num_process):
        AT = int(originalInfo[index])
        BT = int(originalInfo[index + 1])
        process[i] = Process(i, AT, BT, num_process)
        index += 2

    global num_pcores
    num_pcores = pCoreCnt
    global num_ecores
    num_ecores = eCoreCnt

    ShortestProcess = SPN(process, num_process)
    ShortestProcess.Running()
    resultInfo = ShortestProcess.display()
    return resultInfo


# todo : doSRTN
def doSRTN(processNum, originalInfo, pCoreCnt, eCoreCnt):
    global num_process
    num_process = processNum
    process = [0 for i in range(num_process)]
    index = 0
    for i in range(num_process):
        AT = int(originalInfo[index])
        BT = int(originalInfo[index + 1])
        process[i] = Process(i, AT, BT, num_process)
        index += 2

    global num_pcores
    num_pcores = pCoreCnt
    global num_ecores
    num_ecores = eCoreCnt

    ShortestRemaining = SRTN(process, num_process)
    ShortestRemaining.Running()
    resultInfo = ShortestRemaining.display()
    return resultInfo


# todo : doHRRN
def doHRRN(processNum, originalInfo, pCoreCnt, eCoreCnt):
    global num_process
    num_process = processNum
    process = [0 for i in range(num_process)]
    index = 0
    for i in range(num_process):
        AT = int(originalInfo[index])
        BT = int(originalInfo[index + 1])
        process[i] = Process(i, AT, BT, num_process)
        index += 2

    global num_pcores
    num_pcores = pCoreCnt
    global num_ecores
    num_ecores = eCoreCnt

    HighRatio = HRRN(process, num_process)
    HighRatio.Running()
    resultInfo = HighRatio.display()
    return resultInfo

# todo : doBOSS
def doBOSS(processNum, originalInfo, pCoreCnt, eCoreCnt):
    global num_process
    num_process = processNum
    process = [0 for i in range(num_process)]
    index = 0
    for i in range(num_process):
        AT = int(originalInfo[index])
        BT = int(originalInfo[index + 1])
        process[i] = Process(i, AT, BT, num_process)
        index += 2

    global num_pcores
    num_pcores = pCoreCnt
    global num_ecores
    num_ecores = eCoreCnt

    if num_pcores == 0 or num_pcores + num_ecores == 1:
        spn = SPN(process, num_process)
        spn.Running()
        return spn.display()
    else:
        boss = BOSS(process, num_process)
        boss.Running()
        return boss.display()
