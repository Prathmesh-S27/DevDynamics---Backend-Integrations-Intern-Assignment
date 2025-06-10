@echo off
echo 🧪 Running Smart Event Planner Tests...

REM Check if containers are running and start if needed
docker-compose ps | findstr "web.*Up" >nul
if errorlevel 1 (
    echo Starting containers...
    docker-compose up -d
    echo Waiting for services to be ready...
    timeout /t 10 /nobreak > nul
)

REM Run tests
echo Running pytest...
docker-compose exec web pytest tests/ -v

echo ✅ Tests completed!
pause
