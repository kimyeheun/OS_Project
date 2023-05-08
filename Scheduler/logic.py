# 프로세스 개수, 타임 퀀텀, [AT, BT], p코어 개수, e코어 개수, 알고리즘 종류
from Scheduler.Algorithm import doRR


def doAlgorithm(processCnt, quantum, originalInfo, PCoreCnt, ECoreCnt, algorithm):
    print(algorithm)

    if algorithm == 'RR':
        return doRR(processCnt, quantum, originalInfo, PCoreCnt, ECoreCnt)

    # todo: 알고리즘 연결 하기
    # elif algorithm == 'FCFS':
    #     # return doFCFS(processCnt, quantum, originalInfo, PCoreCnt, ECoreCnt)
    # elif algorithm == 'SPN':
    #
    # elif algorithm == 'SRTN':
    #
    # elif algorithm == 'HRRN':
    #
    # else: # MyAlgorithm




