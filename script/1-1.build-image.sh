docker rmi jnuho/fe-nginx
docker rmi jnuho/be-go
docker rmi jnuho/be-py

docker build -f ../dockerfiles/Dockerfile-nginx -t jnuho/fe-nginx ..
docker build -f ../dockerfiles/Dockerfile-go -t jnuho/be-go ..
docker build -f ../dockerfiles/Dockerfile-py -t jnuho/be-py ..
