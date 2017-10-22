docker build -t jindongh/sandbox .
docker run -d -p 10000:10000 jindongh/sandbox

# Debug
docker ps
docker exec -it <container id> /bin/bas
