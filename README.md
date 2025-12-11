to start the program,
enter the following commands:
cd Edu-Archive
.venv/Scripts/Activate.ps1
python main.py


to launch the database, following were executed
pip install email-validator flask flask-login flask-sqlalchemy flask-wtf gunicorn psycopg2-binary wtforms python-dotenv
if (Test-Path venv\Scripts\activate.ps1) { & venv\Scripts\activate.ps1; python reset_admin.py } else { Write-Host "Please activate your virtual environment first: .\venv\Scripts\activate" }
if (Test-Path .venv\Scripts\activate) { .\.venv\Scripts\activate; python reset_admin.py } elseif (Test-Path venv\Scripts\activate) { .\venv\Scripts\activate; python reset_admin.py } else { python reset_admin.py }
Get-Content .env 
python reset_admin.py 
if (Test-Path .env) { Get-Content .env } else { Write-Host "No .env file found" }                                        
python init_admin.py
psql -U postgres -h localhost     
Get-Content .env | ForEach-Object {                                               
>>     if ($_ -and $_ -notmatch '^\s*#') {                                                                               
>>         $name,$val = $_ -split '=',2
>>         Set-Item -Path Env:$name -Value $val
>>     }
>> }
psql -U postgres -h localhost -c "CREATE DATABASE edu_archive;"
pip install --upgrade pip                                                         
>> pip install email-validator flask flask-login flask-sqlalchemy flask-wtf gunicorn psycopg2-binary wtforms python-dotenv
Get-ChildItem Env:
set -a; Get-Content .env | ForEach-Object { if ($_ -and $_ -notmatch '^\s*#') { $name,$val = $_ -split '=',2; Set-Item -Path Env:$name -Value $val } }; set +a                                             
>> python init_admin.py
 flask --app app.py db-create
flask db init
setx DATABASE_URL "sqlite:///edu_archive.db"
   
