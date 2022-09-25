# Anomaly-Detection

trim_video.py 사용법
---
```bash
CatchUP-Anomaly-Detection
├── .git
├── data
│   └── video
│       ├── assult(폭행)
│       ├── burglary(절도)
│       ├── swoon(실신)
│       └── kidnap(납치)
│           └── 199-1
│   
├── main.ipynb
├── README.md
└── ...
```
위와 같은 파일 구조에서 199-1 폴더에 저장된 CCTV 영상을 자르는 코드
편집된 영상은 output 폴더에 저장된다.
``` python
! python trim_video.py -s "data/video/kidnap/199-1" -d "output"
```

