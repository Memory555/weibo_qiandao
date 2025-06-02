@echo off
REM 初始化 Conda 环境变量（第一次运行 Conda）
CALL E:\Anaconda\Scripts\activate.bat

REM 激活你的虚拟环境
CALL conda activate file

REM 切换到脚本所在目录
cd /d C:\Lars

REM 执行脚本
python auto_signin.py

REM 可选：保存日志
REM python auto_signin.py >> signin_log.txt 2>&1

pause
