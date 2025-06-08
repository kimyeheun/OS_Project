# **Process Scheduling** (OS_Project)

## 📝**Project Description**
This project is made for the **Operating Systems** course at the Korea University of Technology and Engineering (*KOREATECH*). The project is a web site that can be used to make a Gantt Chart about the **process scheduling** algorithms.

## 🗓️**Development Period**
2023.03.28. ~ 2023.05.12.

## 👤**Team Members**
* 김가람 *Kim Garam*
  - 컴퓨터공학부 *Computer Science and Engineering* - 21학번
  - [<img src="https://img.shields.io/badge/garamkim83-181717?style=flat&logo=github&logoColor=white"/>](https://github.com/garamkim83)
* 김예은 *Kim Yeheun*
  - 컴퓨터공학부 *Computer Science and Engineering* - 21학번
  - [<img src="https://img.shields.io/badge/kimyeheun-181717?style=flat&logo=github&logoColor=white"/>](https://github.com/kimyeheun)
* 이채린 *Lee Chaerin*
  - 컴퓨터공학부 *Computer Science and Engineering* - 20학번
  - [<img src="https://img.shields.io/badge/Rix01-181717?style=flat&logo=github&logoColor=white"/>](https://github.com/Rix01)
* 임지수 *Lim Jisu*
  - 컴퓨터공학부 *Computer Science and Engineering* - 21학번
  - [<img src="https://img.shields.io/badge/jjimongs-181717?style=flat&logo=github&logoColor=white"/>](https://github.com/jjimongs)

## 🔗**URL**
[Simulator - BOSS](https://bossalgorithmario.pythonanywhere.com)

## ⚙️**Tech Stack**
### Languages & Frameworks
<img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white"/> <img src="https://img.shields.io/badge/CSS-1572B6?style=flat&logo=CSS3&logoColor=white"/> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=JavaScript&logoColor=white"/> <img src="https://img.shields.io/badge/jQuery-0769AD?style=flat&logo=jquery&logoColor=white"/> <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white"/>

### Tools
<img src="https://img.shields.io/badge/PyCharm-000000?style=flat&logo=PyCharm&logoColor=white"/> <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white"/> <img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white"/> <img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white"/>

## 👓 **Pre-View**
![image](https://github.com/user-attachments/assets/98d0a7a0-3a21-4b66-81aa-c839edb895c7)

①  (+) 버튼을 눌러 프로세스를 추가할 수 있다. 그리고 프로세스마다 AT와 BT를 입력할 수 있다.

②  Core 박스에서 각 코어를 의미하는 버튼을 눌러서 코어의 종류를 정할 수 있다. 초기 상태는 OFF이다. OFF 상태인 코어를 한 번 누르면 PCORE로 변경되고, PCORE 상태인 코어를 한 번 더 누르면 ECORE로 변경된다. 이 정보는 Core 박스 아래의 최하단 부분에 있는 Processor 정보에 자동으로 업데이트된다.

③  적용할 스케줄링 알고리즘을 선택할 수 있다. RR을 선택하면 박스 하단에 time quantum을 적용할 수 있는 창이 추가된다. BOSS를 선택하면 우리 팀이 만든 알고리즘을 실행할 수 있다.

④  여기에서 시뮬레이션 로그를 확인할 수 있다. 이전에 실행한 시뮬레이션 정보들이 저장되며 각 버튼을 누르면 이전 기록을 볼 수 있다.

⑤  선택한 스케줄링 알고리즘의 설명을 확인할 수 있다.

⑥  Go! 버튼을 눌러 시뮬레이션을 진행할 수 있다. 시뮬레이션 과정이 끝나면 자동으로 다음 화면으로 넘어간다.


![image01](https://github.com/user-attachments/assets/73d1b606-bdeb-423a-bccd-bb5fe6d34c75)
①  스케줄링 과정에 따라 계산된 결과를 확인할 수 있다. AT, BT, WT, TT, NTT를 한 화면에서 확인할 수 있다.

②  코어들이 프로세스를 처리하면서 소모하는 전력량을 확인할 수 있다.

③  스케줄링하여 결과로 도출된 간트 차트를 확인할 수 있다. 간트 차트의 가로 길이가 상자보다 길어지면 간트 차트 아래에 스크롤바가 생겨 옆으로 넘길 수 있게 만들었다.

④  다운로드 버튼을 누르면 이 화면에 있는 정보들을 png 파일로 저장할 수 있다. 스케줄링을 통해 계산된 결과값(왼쪽 파란색 상자), 전력 소모량(오른쪽 위 노란색 상자), 간트 차트(오른쪽 아래 초록색 상자)가 각각 다른 파일로 저장된다.

<!-- 아이콘은 여기서 https://simpleicons.org/ -->
