$(document).ready(function () {
    $("#goButton").click(function () {
        // 프로세스 개수 받아오기
        // var processorCnt = parseInt(prompt("Enter the number of processors:"));
        // var endTime = parseInt(prompt("Enter the end time:"));
        // var processCnt = parseInt(prompt("Enter the number of processes:"));

        var processorCnt = 4;
        // pcore ecore의 배치는 for문으로 받아오기
        var pcoreCnt = 2;
        var ecoreCnt = 2;
        var cores = ["Pcore1", "Pcore2", "Ecore1", "Ecore2"];

        var endTime = 13;
        var processCnt = 6;

        var colors = []
        for (var i = 1; i <= processCnt; i++) {
            colors.push(getRandColor());
        }
        // 각 시간당 각 프로세서에서 어떤 프로세스가 동작하는가
        var processes =
            [[1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 2, 0, 0],
            [1, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 3, 0],
            [0, 0, 3, 4],
            [0, 0, 3, 4],
            [5, 0, 3, 4],
            [5, 6, 3, 4],
            [0, 6, 3, 4],
            [0, 6, 3, 0],
            [0, 6, 0, 0]];

        // 간트차트로 쓰일 테이블 생성
        var ganttTable = $("<table id='ganttTable'>");

        // 시간 스탬프 표시
        var timeRow = $("<tr class='tableRow' id='tableRow'>");
        for (var i = 0; i <= endTime; i++) {
            if (i == 0) timeRow.append("<th style='width:100px; background:#FFFFFF'></th>");
            else timeRow.append("<th class='timeStamp' id='timeStamp'>" + i + "</th>");
        }
        ganttTable.append(timeRow);

        for (var i = 0; i < processorCnt; i++) {
            var col = $("<tr class='tableCol' id='tableCol'>");
            col.append("<td class='innerHeader' id='innerHeader'>" + cores[i] + "</td>");
            for (var j = 0; j < endTime; j++) {
                if (processes[j][i] != 0) {
                    if (j == 0 || (j > 0 && processes[j - 1][i] != processes[j][i]))
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

function getRandColor() {
    // 랜덤으로 하기 vs 정해진 색 n개 만들어 놓기
    // #FFFFFF의 형태로 랜덤 색상 반환
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}