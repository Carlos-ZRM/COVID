sudo docker rm -f covid-app 
sudo docker image rm -f  covid-image
sudo docker build --tag covid-image .
sudo docker run  -it --name covid-app -v app:/app -p 5000:5000 covid-image
