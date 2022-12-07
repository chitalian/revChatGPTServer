```
virtualenv env
source env/bin/activate

pip install -r requirements.txt

# Run locally
uvicorn main:app --reload

# Run in prod
python main.py
```
