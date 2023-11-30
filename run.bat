@echo off
set modes=start-dev stop-dev interactive-dev check-syntax
set mode=%1
set project_name=alumni-portal

if "%project_name%"=="*****" (
    echo Please Update the Project Name in run.bat
    exit /b 0
)

if "%mode%"=="" (
    echo Invalid mode
    echo Please enter one of the following mode:
    echo %modes%
) else if "%mode%"=="start-dev" (
    docker-compose -p %project_name%-dev -f docker-compose-dev.yml build
    docker-compose -p %project_name%-dev -f docker-compose-dev.yml up -d
) else if "%mode%"=="stop-dev" (
    docker-compose -p %project_name%-dev -f docker-compose-dev.yml down
) else if "%mode%"=="interactive-dev" (
    docker exec -it --user root %project_name%-backend bash
) else if "%mode%"=="check-syntax" (
    docker exec -it --user root %project_name%-backend flake8 .
) else (
    echo Invalid mode
    echo Please enter one of the following mode:
    echo %modes%
)
