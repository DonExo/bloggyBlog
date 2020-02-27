# bloggyBlog

### an entry project for OfficeApp - Netherlands

Steps to successfully run this project:
1. Clone/download this repo locally
2. Create virtual env with python3 (at least 3.6) as interpreter 
`mkvirtualenv --python='which python3' venv` (replace ' with `)
3. Install the requirements
`pip install requirements.txt`
4. Run migrations (this will create local sqlite db)
`./manage.py migrate`
5. Optional: Load fixtures if you don't want to input data yourself
`./manage.py loaddata fixtures.json`
6. Run the server (optionally with a port)
`./manage.py runserver {port}`
7. Visit "http://localhost:8000/admin" and log-in with user/pass: admin