# For development use (simple logging, etc):
python app/server.py
# For production use: 
# gunicorn server:app -w 1 --log-file -