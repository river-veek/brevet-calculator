docker stop $(docker container ls --format {{.ID}})
docker rm $(docker container ls --format {{.ID}})
docker container ls
docker rmi $(docker images --filter=reference="flask-app" --format {{.ID}})
docker images
