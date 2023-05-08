$(document).ready(function () {
    $("#gantt").click(function () {
        console.log("this is gantt");

        // take Info
        let info = document.getElementById('current').innerText;
        let sliceInfo = info.split(" ");
        let ganttInfo = document.getElementById('ganttInfo-timeTable').innerText;
        let ganttFT = document.getElementById('ganttInfo-finishTime').innerText;

        // set Variable
        let pcoreCnt = parseInt(sliceInfo[7]);
        let ecoreCnt = parseInt(sliceInfo[12]);
        let processCnt = parseInt(sliceInfo[2]);
        let processorCnt = pcoreCnt + ecoreCnt;  // 얘는 pCoreCnt + eCoreCnt 값
        let endTime = parseInt(ganttFT);   // FT

        // todo : 이차원 배열 넣기
        // 각 시간당 각 프로세서에서 어떤 프로세스가 동작하는가
        console.log("what?");
        console.log(ganttInfo);
        console.log(endTime);
        let processes = JSON.parse(ganttInfo);
        console.log(processes);

        // set Core List
        let cores;
        (cores = []).length = processorCnt;
        cores.fill(0);

        let idx = 0;
        for(let i = 1; i <= pcoreCnt; i++) {
            cores[idx++] = "PCore" + i;
        }
        for(let i = 1; i <= ecoreCnt; i++) {
            cores[idx++] = "ECore" + i;
        }

        // choose random color
        let colors = []
        for (let i = 0; i <= processCnt; i++) {
            colors.push(getRandColor());
        }


        // 간트차트로 쓰일 테이블 생성
        let ganttTable = $("<table id='ganttTable'>");

        // 시간 스탬프 표시
        let timeRow = $("<tr class='tableRow' id='tableRow'>");
        for (let i = 0; i <= endTime+1; i++) {
            if(i === endTime+1) timeRow.append("<th style='width:20px; background:#FFFFFF'></th>");
            else if (i === 0) timeRow.append("<th style='width:120px; background:#FFFFFF'></th>");
            else timeRow.append("<th class='timeStamp' id='timeStamp'>" + i + "</th>");
        }
        ganttTable.append(timeRow);

        // 칠하기
        for (let i = 0; i < processorCnt; i++) {
            let col = $("<tr class='tableCol' id='tableCol'>");
            col.append("<td class='innerHeader' id='innerHeader'>" + cores[i] + "</td>");
            for (let j = 0; j <= endTime; j++) {
                if (j === endTime) col.append("<td style = 'width:2%' ></td>");

                else if (processes[j][i] !== 0) {
                    if (j === 0 || (j > 0 && processes[j - 1][i] !== processes[j][i]))
                        col.append("<td style='background-color:" + colors[processes[j][i]] + ";'>P" + processes[j][i] + "</td>");
                    else
                        col.append("<td style='background-color:" + colors[processes[j][i]] + ";'></td>");
                }
                else col.append("<td></td>");
            }
            ganttTable.append(col);
        }

        // add the table to the chart container
        $("#baseTable").html(ganttTable);
    });
});

// function drawGanttChart(gantT ,myFT) {
//     console.log("this is gantt");
//         // 프로세스 개수 받아오기
//         // var processorCnt = parseInt(prompt("Enter the number of processors:"));
//         // var endTime = parseInt(prompt("Enter the end time:"));
//         // var processCnt = parseInt(prompt("Enter the number of processes:"));
//
//         let info = document.getElementById('current').innerText;
//         console.log('info', info);
//         let sliceInfo = info.split(" ");
//
//         let pcoreCnt = parseInt(sliceInfo[7]);
//         let ecoreCnt = parseInt(sliceInfo[12]);
//         console.log("p",pcoreCnt, "e", ecoreCnt);
//         let processorCnt = pcoreCnt + ecoreCnt;  // 얘는 pCoreCnt + eCoreCnt 값
//
//         let cores;
//         (cores = []).length = processorCnt;
//         cores.fill(0);
//
//         let idx = 0;
//         for(let i = 1; i <= pcoreCnt; i++) {
//             cores[idx++] = "PCore" + i;
//         }
//         for(let i = 1; i <= ecoreCnt; i++) {
//             cores[idx++] = "ECore" + i;
//         }
//
//         // FT
//         let endTime = myFT;
//         // 시뮬레이터 인포에서 값 가져오기 (ProcessCnt)
//         let processCnt = parseInt(sliceInfo[2]);
//
//         let colors = []
//         for (let i = 0; i <= processCnt; i++) {
//             colors.push(getRandColor());
//         }
//
//         console.log("gantt : ", gantT);
//         console.log("FT :", myFT);
//
//         // todo : 이차원 배열 넣기
//         // 각 시간당 각 프로세서에서 어떤 프로세스가 동작하는가
//         let processes = gantT;
//
//         // 간트차트로 쓰일 테이블 생성
//         let ganttTable = $("<table id='ganttTable'>");
//
//         // 시간 스탬프 표시
//         let timeRow = $("<tr class='tableRow' id='tableRow'>");
//         for (let i = 0; i <= endTime; i++) {
//             if (i === 0) timeRow.append("<th style='width:120px; background:#FFFFFF'></th>");
//             else timeRow.append("<th class='timeStamp' id='timeStamp'>" + i + "</th>");
//         }
//         ganttTable.append(timeRow);
//
//         // 칠하기
//         for (let i = 0; i < processorCnt; i++) {
//             let col = $("<tr class='tableCol' id='tableCol'>");
//             col.append("<td class='innerHeader' id='innerHeader'>" + cores[i] + "</td>");
//             for (let j = 0; j < endTime; j++) {
//                 if (processes[j][i] !== 0) {
//                     if (j === 0 || (j > 0 && processes[j - 1][i] !== processes[j][i]))
//                         col.append("<td style='background-color:" + colors[processes[j][i]] + ";'>P" + processes[j][i] + "</td>");
//                     else
//                         col.append("<td style='background-color:" + colors[processes[j][i]] + ";'></td>");
//                 }
//                 else col.append("<td></td>");
//             }
//             ganttTable.append(col);
//         }
//
//         // add the table to the chart container
//         $("#baseTable").html(ganttTable);
// }


function getRandColor() {
    // 랜덤으로 하기 vs 정해진 색 n개 만들어 놓기
    // #FFFFFF의 형태로 랜덤 색상 반환
    let letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}