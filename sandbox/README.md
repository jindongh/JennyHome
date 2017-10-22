docker build -t jindongh/sandbox .
docker run -d -p 4000:8080 jindongh/sandbox

# Debug
docker ps
docker exec -it <container id> /bin/bas
