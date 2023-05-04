# crete virtual environment
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

#start api server
uvicorn app.main:app --reload