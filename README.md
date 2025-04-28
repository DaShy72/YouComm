# YouComm
This project is for processing and analyzing data (comments from a specific video)

## How to start a project

1. Clone the repository:
   ```bash
   git clone https://github.com/DaShy72/YouComm.git
   cd youtube_comment_parser
2. Create a virtual environment:
  python -m venv venv
source venv/Scripts/activate   # Windows

3. Install dependencies:
  pip install -r requirements.txt

4. Apply migrations:
  python manage.py migrate

5. Start the server:
  python manage.py runserver
