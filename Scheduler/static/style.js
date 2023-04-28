/**
 * add Processor
 * @type {number}
 */
let processCount = 2;

function addProcessor() {
    // table element 찾기
    const table = document.getElementById('processOne');

    let row = table.insertRow(table.rows.length);
    let processName = row.insertCell(0);
    let at = row.insertCell(1);
    let bt = row.insertCell(2);

    processName.innerHTML =  '<td id="realName">Process'+processCount+' (P'+processCount+')</td>';
    at.innerHTML = '<td id="realAt"><input type="text" name="arrivalTime" required size="10"></td>';
    bt.innerHTML = '<td id="realBt"><input type="text" name="burstTime" required size="10"></td>';

    processCount++;

    setProcessInfo();

    if(processCount === 19) {
        const btn = document.getElementById('plus');
        if(btn.style.display !== 'none') {
            btn.style.display = 'none';
        }
    }
}

function addSimulator() {
    const table = document.getElementById('Logs');

    let row = table.insertRow(table.rows.length);
    let process = row.insertCell(0);

    process.innerHTML = '<td id="logName"><button id = "logButton"> hi </button></td>'
}

/**
 * P, E Core
 * @type {number[]}
 */
let checkList = [0, 0, 0, 0];

function changeColor(num) {
    let processId = 'core' + num;
    let changeButton = document.getElementById(processId);

    let check = checkList[num-1] % 3;
    if(check === 0){
        changeButton.style.backgroundColor = "#FFFFFF";
        changeButton.style.color = "#62C184";
        changeButton.style.borderColor = "#62C184";
        changeButton.innerText = "PCORE";
    }
    else if(check === 1){
        changeButton.style.backgroundColor = "#62C184";
        changeButton.style.color = "#FFFFFF";
        changeButton.innerText = "ECORE";
    }
    else {
        changeButton.style.backgroundColor = "#D0EDDA";
        changeButton.innerText = "OFF";
    }

    setCoreInfo(check);

    checkList[num-1] += 1;
    // console.log(checkList[num-1]);
}

/**
 * algorithm explain
 */
function algorithmExplain(e) {
    const text = e.options[e.selectedIndex].text;

    if(text === 'RR (Round Robin)') {
        document.getElementById('explainText1').innerText = "RR 설명이지롱~";
    }
    else if(text === 'FCFS (First Come First Service)') {
        document.getElementById('explainText1').innerText = "FCFS 설명이지롱~";
    }
    else if(text === 'SPN (The Shortest Process Next)') {
        document.getElementById('explainText1').innerText = "SPN 설명이지롱~";
    }
    else {
        document.getElementById('explainText1').innerText = "MyAlgorithm 설명이지롱~";
    }

    algorithm(e);
}

/**
 * drop down algorithm
 */
function algorithm(e) {
    const text = e.options[e.selectedIndex].text;

    if(text === 'RR (Round Robin)' || text === 'MyAlgorithm' ) {
        document.getElementById("RR").style.visibility ='visible';
    }
    else {
        document.getElementById("RR").style.visibility ='hidden';
    }
}

/**
 * Simulator information
 * @type {number}
 */
let processCnt = 0;
function setProcessInfo() {
    const processText = document.getElementsByClassName('processCnt')[0];

    processText.innerText = ++processCnt;
}

let PCoreCnt = 0;
let ECoreCnt = 0;
function setCoreInfo(check) {
    const PCoreText =  document.getElementsByClassName('PCoreCnt')[0];
    const ECoreText = document.getElementsByClassName('ECoreCnt')[0];

    // P->E
    if(check === 0) {
        PCoreText.innerText = ++PCoreCnt;
    }
    //off -> P
    else if(check === 1) {
        PCoreText.innerText = --PCoreCnt;
        ECoreText.innerText = ++ECoreCnt;
    }
    else {
        ECoreText.innerText = --ECoreCnt;
    }

}