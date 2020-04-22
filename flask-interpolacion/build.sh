sudo docker rm -f flask-app 
sudo docker image rm -f  flask-image
sudo docker build --tag flask-image .
sudo docker run  -it --name flask-app -p 5000:5000 flask-image