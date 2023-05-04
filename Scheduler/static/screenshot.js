// html2canvas 라이브러리를 이용하여 스케줄러 화면을 캡쳐하여 이미지로 다운로드하는 기능 구현
var downloadBt = document.getElementById("downloadBt");
downloadBt.addEventListener("click", function () {
  var fileName = null;
  while (fileName == null || fileName=="") {
    fileName = prompt("파일명을 입력하세요.", "process_scheduling_gantt_chart");
    if(fileName == null) return;  // 취소 버튼을 누르면 함수 종료
  }
  
  // 함께 캡쳐되지 않도록 downloadBt를 숨김
  downloadBt.style.display = "none";

  // go를 누른 후 다음 화면으로 넘어갔을 때의 화면을 캡쳐
  html2canvas(document.body, {
    //scale: 1, // 화면 배율
    //backgroundColor: "#ffffff", // 배경색
    x: document.getElementById("chartScreen").offsetLeft,
    y: document.getElementById("chartScreen").offsetTop,
    width: document.getElementById("chartScreen").offsetWidth + 25,
    height: document.getElementById("chartScreen").offsetHeight,

    // 크로스 도메인인가?
    //useCORS: true // 이미지 다운로드할 때 CORS 에러 방지
  }).then(function (canvas) {
    // 이미지 생성 후 downloadBt를 다시 보이게 함
    downloadBt.style.display = "block";

    // 캔버스를 이미지 URL로 변환
    var image = canvas.toDataURL("image/png");

    // a 태그: 하이퍼링크 생성, 다운로드 링크 추가
    var link = document.createElement("a");
    link.download = fileName + ".png";
    link.href = image;

    // a 태그 클릭하여 파일 다운로드
    link.click();
  });
});