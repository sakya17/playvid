Create python virtual environment:
```
python3 -m venv .venv
```

Activate virtual environment:
```
source .venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

To run, copy videos to the same folder with play.py, then run this command:
```
python3 play.py video1.mp4 video2.mp4
```

The output CSV file will have the same name with the first video: video1.mp4_out.csv