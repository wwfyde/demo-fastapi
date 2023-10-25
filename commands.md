```shell
docker build -t demo-fastapi .
docker create network 
docker run -p 8008:8000 --network demo-fastapi -e TZ=Asia/Shanghai --name demo-fastapi -dit demo-fastapi

uvicorn app.main:app --port 8000

```
