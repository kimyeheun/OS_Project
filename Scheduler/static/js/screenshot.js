// 프로세스 스케줄링 시뮬레이터의 화면을 캡쳐하여 png로 저장
document.addEventListener("DOMContentLoaded", function(event) {

  let downloadBt = document.getElementById("downloadBt");

  downloadBt.addEventListener("click", function () {
    // 함께 캡쳐되지 않도록 downloadBt를 숨김
    downloadBt.style.display = "none";

    let simulatorName = "Simulator_" + document.getElementById('simulatorName').innerText;

    // go를 누른 후 다음 화면으로 넘어갔을 때의 화면을 캡쳐
    html2canvas(document.body, {
      x: document.getElementById("performance").offsetLeft,
      y: document.getElementById("performance").offsetTop,
      width: document.getElementById("performance").offsetWidth + 25,
      height: document.getElementById("performance").offsetHeight,

      // 크로스 도메인인가?
      //useCORS: true // 이미지 다운로드할 때 CORS 에러 방지
    }).then(function (canvas) {
      // 이미지 생성 후 downloadBt를 다시 보이게 함
      downloadBt.style.display = "block";

      // 캔버스를 이미지 URL로 변환
      let image = canvas.toDataURL("image/png");

      // a 태그: 하이퍼링크 생성, 다운로드 링크 추가
      let link = document.createElement("a");
      link.download = simulatorName + "_Performance.png";
      link.href = image;

      // a 태그 클릭하여 파일 다운로드
      link.click();
    });

    // 프로세스 테이블 캡쳐
    html2canvas(document.body, {
      x: document.getElementById("leftPart").offsetLeft,
      y: document.getElementById("leftPart").offsetTop,
      width: document.getElementById("leftPart").offsetWidth + 8,
      height: document.getElementById("leftPart").offsetHeight,
    }).then(function (canvas) {
      // 캔버스를 이미지 URL로 변환
      let image = canvas.toDataURL("image/png");

      // a 태그: 하이퍼링크 생성, 다운로드 링크 추가
      let link = document.createElement("a");

      link.download = simulatorName + "_Process_table.png";
      link.href = image;

      // a 태그 클릭하여 파일 다운로드
      link.click();
    });

    html2canvas(document.querySelector("#ganttTable")).then(function (canvas) {
      // 이미지 데이터를 다운로드 링크로 변환
      const link = document.createElement("a");
      link.download = simulatorName + "_Gantt_chart.png";
      link.href = canvas.toDataURL("image/png");
      link.click();
    });
  });
});