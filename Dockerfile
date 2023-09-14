# 使用 Python 官方映像作為基礎映像
FROM python:3.8-slim

# 安裝 Discord.py
RUN pip install --upgrade pip
RUN pip install discord.py
# 複製你的 Discord Python 程式到 Docker 容器內
COPY dc.py /app/dc.py

# 設定工作目錄
WORKDIR /app

# 執行你的 Discord Python 程式
CMD ["python", "dc.py"]

