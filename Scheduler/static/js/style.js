/**
 * P, E Core - Color Change
 * @type {number[]}
 */
let checkList = [0, 0, 0, 0];
let check = 0;
function changeColor(num) {
    let processId = 'core' + num;
    let changeButton = document.getElementById(processId);

    check = checkList[num-1] % 3;
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
}


/**
 * algorithm explain
 */
function algorithmExplain(e) {
    const text = e.options[e.selectedIndex].text;
    algorithmExplainShow(text);
    algorithm(e);
}

document.addEventListener("DOMContentLoaded", function(event) {
    let text = document.getElementById('explainText1').innerText;
    algorithmExplainShow(text);
    algorithmShow(text);
});

function algorithmExplainShow(text) {
    if(text === 'RR (Round Robin)' || text === 'RR') {
        document.getElementById('explainText1').innerText =
            "[RR(Round-Robin)]\n 먼저 도착한 프로세스를 먼저 처리 해주되, 자원 사용 제한 시간(time quantum)이 있는 스케줄링 알고리즘\n\n" +
            "[Preemptive scheduling]\n 각각의 프로세스는 타의에 의해 할당 받은 자원을 처리 도중 빼앗길 수 있음\n\n" +
            "프로세스는 할당된 시간이 지나면 자원을 반납하게 되어 자원 독점을 방지함\n\n" +
            "대화형 시스템, 시분할 시스템에 적합";
    }
    else if(text === 'FCFS (First Come First Service)' || text === 'FCFS') {
        document.getElementById('explainText1').innerText =
            "[First Come First Service]\n먼저 도착한 프로세스를 먼저 처리해주는 스케줄링 알고리즘\n\n" +
            "[Non-preemptive scheduling]\n 각각의 프로세스는 할당 받은 자원을 스스로 반납할 때까지 사용 가능\n\n" +
            "Context switch overhead가 적고 자원을 효율적으로 사용할 수 있음\n\n" +
            "먼저 온 프로세스의 수행시간이 긴 경우 다른 프로세스들이 긴 대기시간을 가지게 되는 Convoy effect가 발생할 수 있어 비교적 긴 평균 응답시간을 가짐";
    }
    else if(text === 'SPN (Shortest Process Next)' || text === 'SPN') {
        document.getElementById('explainText1').innerText =
            "[Shortest Process Next]\nburst time이 작은 순으로 프로세스들을 처리하는 스케줄링 알고리즘\n\n" +
            "[Non-preemptive scheduling]\n 각각의 프로세스는 할당 받은 자원을 스스로 반납할 때까지 사용 가능\n\n" +
            "평균 대기시간을 최소화하고 시스템 내 프로세스 수를 최소화 할 수 있다는 장점이 있지만 " +
            "burst time이 긴 프로세스의 경우 자원을 할당 받지 못 하는 starvation 현상이 발생할 수 있음";
    }
    else if(text === 'HRRN (Highest Response Ratio Next)' || text === 'HRRN') {
        document.getElementById('explainText1').innerText =
            "[High Response Ratio Next]\nSPN에 Aging concepts를 적용한 스케줄링 알고리즘\n\n" +
            "[Non-preemptive scheduling]\n각각의 프로세스는 할당 받은 자원을 스스로 반납할 때까지 사용 가능\n\n" +
            "Response Ratio {(WT+BT)/BT}가 클수록 빠른 처리 순서를 가짐\n\n" +
            "SPN의 장점과 Starvation을 방지할 수 있다는 장점이 있지만 " +
            "실행시간 예측 기법이 필요하여 overhead가 발생";
    }
    else if(text === 'SRTN (Shortest Remaining Time Next)'|| text === 'SRTN') {
        document.getElementById('explainText1').innerText =
            "[Shortest Remaining Time Next]\nSPN의 변형. 잔여 시간이 더 적은 프로세스가 ready 상태가 되면 선점되는 스케줄링 알고리즘\n\n" +
            "[Preemptive scheduling]\n각각의 프로세스는 타의에 의해 할당 받은 자원을 처리 도중 빼앗길 수 있음\n\n" +
            "SPN의 장점을 극대화할 수 있지만 프로세스 생성 시 총 실행 시간 예측이 필요하고, 잔여 실행을 계속 추적해야 하므로 overhead가 큼\n\n";
    }
    else if(text === 'BOSS Algorithm') {
        document.getElementById('explainText1').innerText =
            "[BOSS Algorithm]\n" +
            "\n{Core의 수가 2개 이상일 때} " +
            "\nBT 기준으로 정렬하여 Ready Queue에 삽입" +
            "\nECore : BT가 짧은 순서로 할당" +
            "\nPCore : BT가 긴 순서로 할당" +
            "\n\n{Core의 수가 1개일 때} " +
            "\nSPN 방식 (WT를 최소화)" +
            "\n\n* PCore만 있을 때는 BT가 가장 짧은 프로세스를 먼저 처리하여 WT의 합이 길어지는 것을 방지\n" +
            "이처럼 Core 개수에 따라 알고리즘의 동작을 다르게 하여 효율적으로 동작하도록 함*";
    }
    else {
        document.getElementById('explainText1').innerText = "";
    }
}


/**
 * dropDown algorithm - Choose Algorithm with RR
 */
function algorithm(e) {
    const text = e.options[e.selectedIndex].text;
    algorithmShow(text);
}
function algorithmShow(text){
    if(text === 'RR (Round Robin)' || text==='RR' ) {
        document.getElementById("RR").style.visibility ='visible';
    }
    else {
        document.getElementById("RR").style.visibility ='hidden';
    }
}

/**
 * Simulator Information
 * @type {number}
 */
let pcoreCnt = 0;
let ecoreCnt = 0;

function setCoreInfo(check) {
    const PCoreText =  document.getElementsByClassName('PCoreCnt')[0];
    const ECoreText = document.getElementsByClassName('ECoreCnt')[0];

    pcoreCnt = pcoreCount(check);
    ecoreCnt = ecoreCount(check);

    PCoreText.value = pcoreCnt;
    ECoreText.value = ecoreCnt;
}

function pcoreCount(check) {
    if(check === 1) {
        return --pcoreCnt;
    }
    else if(check === 2) return pcoreCnt;
    return ++pcoreCnt;
}
function ecoreCount(check) {
    if(check === 2) {
        return --ecoreCnt;
    }
    else if(check === 0) return ecoreCnt;
    return ++ecoreCnt;
}


/**
 * add Process
 */
let processCnt = 1;
let processName_cnt = 1;
document.addEventListener("DOMContentLoaded", function(event) {
    let addButton = document.querySelector('#plus');
    addButton.addEventListener('click', addProcess);

    function addProcess(e) {
        let processForm = document.querySelectorAll(".process-form");
        let container = document.querySelector('#form-container');
        let totalForms = document.querySelector('#id_form-TOTAL_FORMS');

        let formNum = processForm.length - 1;

        e.preventDefault();

        let newForm = processForm[processCnt - 1].cloneNode(true);
        let formRegex = RegExp(`form-(\\d{1,2})-`, 'g');

        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);

        // input 폼 추가
        container.insertBefore(newForm, addButton);
        totalForms.setAttribute('value', `${formNum + 1}`);

        //프로세스 이름 변경
        let processNameSpan = newForm.querySelector('#processName');
        processNameSpan.innerText = "Process " + ++processName_cnt;

        // 프로세스 개수 늘리기
        const ProcessText = document.getElementsByClassName('processCnt')[0];
        processCnt++;
        ProcessText.value = processCnt;

        // 프로세스 개수가 18개가 되면 '+' 버튼 안 보이게
        if (processCnt === 18) {
            const plusButton = document.getElementById("plus");
            plusButton.style.display = 'none';
        }
    }
});


/**
 * simulator information - get variable
 */
$('input[name=processCnt]').attr('value',processCnt);
$('input[name=PCoreCnt]').attr('value',pcoreCnt);
$('input[name=ECoreCnt]').attr('value',ecoreCnt);


/**
 * assemble 3 forms & submit
 */
$(document).ready(function() {
  $('#goButton').click(function() {
    let formData = new FormData();

    let processNum = $('#current-simulator').serialize();
    let PCoreNum = $('#AlgorithmList').serialize();
    let ECoreNum = $('#form-container').serialize();

    processNum += '&' + PCoreNum + '&' + ECoreNum;
    formData.append('QueryDict', processNum);

    $.ajax({
      url: '',
      type: 'POST',
      data: formData,
      async: false,
      contentType: false,
      processData: false,
      success: function(response) {
          window.location.href = `http://127.0.0.1:8000${response}`;
      },
      error: function(xhr, status, error) {
          let errorMsg;
          if (xhr.responseText.length > 30)
              errorMsg = "간트 차트를 불러오는 과정에서 문제가 발생했습니다.\n";
          else errorMsg = xhr.responseText+'\n';

          alert(errorMsg + '다시 만들어 주세요.');
          window.location.href = 'http://127.0.0.1:8000';
      }
    });
  });
});

/**
 * Input Field Valid Check - Only Number
 */
function handleInputChange() {
    this.value = this.value.replace(/[^0-9]/g, '');
}

$(document).ready(function() {
    $("input[type='text']").on('input', handleInputChange);
    $(document).on('input', "input[type='text']", handleInputChange); //새로 추가 되는 input 태그

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
            }
        }
    });
});


/**
 * showLog.html - Core Color Change
 * @param button
 * @param cnt
 */
function changeColorLog(button, cnt) {
    if(cnt === 0){
        button.style.backgroundColor = "#FFFFFF";
        button.style.color = "#62C184";
        button.style.borderColor = "#62C184";
        button.innerText = "PCORE";
    }
    else if(cnt === 1){
        button.style.backgroundColor = "#62C184";
        button.style.color = "#FFFFFF";
        button.innerText = "ECORE";
    }
    else {
        button.style.backgroundColor = "#D0EDDA";
        button.innerText = "OFF";
    }
}
document.addEventListener("DOMContentLoaded", function() {
    const PcoreNum = document.getElementById('PCoreInfo').textContent;
    const EcoreNum = document.getElementById('ECoreInfo').textContent;

    let p = PcoreNum;
    let e = EcoreNum;
    for (let c = 1; c <= 4; c++) {
        let coreName = 'core' + c;
        const button = document.getElementById(coreName);

        if (parseInt(p) !== 0) {
            changeColorLog(button, 0);
            p--;
        }
        else if (parseInt(e) !== 0) {
            changeColorLog(button, 1);
            e--;
        }
    }
});


/**
 * scroll down & draw Gantt Chart
 */
window.onload = function () {
    let target = document.getElementById("chartScreen");
    let btn = document.getElementById('gantt');
    if (target !== null) {
        target.scrollIntoView({ behavior: 'smooth' });
        btn.click();
    }
}


/**
 *  show Information - How to use this Site
 */
document.addEventListener("DOMContentLoaded", function() {
    let InfoBtn = document.getElementById('InfoButton');
    let HowToUse = document.getElementById('Information');
    let closeHowToUse = document.getElementById('closeHowToUse');

    if (InfoBtn != null) {
        InfoBtn.onclick = function () {
            HowToUse.style.display = 'block';
        }
        closeHowToUse.onclick = function () {
            HowToUse.style.display = 'none';
        }
    }

    window.onclick = function(event) {
        if (event.target == HowToUse) {
            HowToUse.style.display = "none";
        }
    }
});
