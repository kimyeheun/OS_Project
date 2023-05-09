from Scheduler.Algorithm import doRR, doFCFS, doSRTN, doSPN, doHRRN, doBOSS


# 프로세스 개수, 타임 퀀텀, [AT, BT], p코어 개수, e코어 개수, 알고리즘 종류
def doAlgorithm(processCnt, quantum, originalInfo, PCoreCnt, ECoreCnt, algorithm):
    if algorithm == 'RR':
        return doRR(processCnt, quantum, originalInfo, PCoreCnt, ECoreCnt)
    elif algorithm == 'FCFS':
        return doFCFS(processCnt, originalInfo, PCoreCnt, ECoreCnt)
    elif algorithm == 'SPN':
        return doSPN(processCnt, originalInfo, PCoreCnt, ECoreCnt)
    elif algorithm == 'SRTN':
        return doSRTN(processCnt, originalInfo, PCoreCnt, ECoreCnt)
    elif algorithm == 'HRRN':
        return doHRRN(processCnt, originalInfo, PCoreCnt, ECoreCnt)
    else:  # BOSSAlgorithm
        return doBOSS(processCnt, originalInfo, PCoreCnt, ECoreCnt)
