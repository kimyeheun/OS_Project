$(document).ready(function () {
    var numProcessors = 4;
    // 몇 W 사용
    var pw = [2, 2, 2, 2];
    // 몇 % 사용
    var pper = [2, 2, 2, 2];

    for (var i = 0; i < numProcessors; i++) {
        var performaneBubble = document.createElement("div");
        performaneBubble.setAttribute("class", "performanceBubble");
        performaneBubble.setAttribute("id", "performanceBubble");

        var processorDiv = document.createElement("div");
        processorDiv.setAttribute("class", "processorPerformOne");
        processorDiv.setAttribute("id", "processorPerformOne");
        processorDiv.innerHTML = "Processor " + (i+1);
        processorDiv.setAttribute("style", "font-size: 25pt;");

        // 새로운 테이블 엘리먼트 생성
        var table = document.createElement("table");
        table.setAttribute("class", "newTable");

        var tr = document.createElement("tr");
        tr.setAttribute("class", "newTr");
        tr.setAttribute("style", "display: flex; flex-direction: row;");

        var td1 = document.createElement("td");
        td1.setAttribute("class", "newTd");
        td1.setAttribute("style", "margin-right: 50px;");
        td1.innerHTML = pw[i] + "W";

        var td2 = document.createElement("td");
        td2.setAttribute("class", "newTd");
        td2.innerHTML = pper[i] + "%";

        tr.append(td1);
        tr.append(td2);
        table.append(tr);

        // processorDiv에 새로운 테이블 추가
        performaneBubble.append(processorDiv);
        performaneBubble.append(table);
        $("#processorPerforms").append(performaneBubble);
    }
});