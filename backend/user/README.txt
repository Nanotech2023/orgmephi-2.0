1. Install requirements from requirements.txt
    pip install -r requirements.txt

2. Generate RSA key pair (id_rsa and id_rsa.pub) in "user" directory
    ssh-keygen -t rsa -m PEM

3. Set environment variables
    export FLASK_APP=orgmephi_user/__init__.py
    export ORGMEPHI_AUTH_CONFIG=/path/to/config.py

4. Run server script (from "user" directory)
    python -m flask run --port <port>