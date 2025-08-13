# Docker: create image

Purpose: build and run the `Aqua Nova` example site in Docker.

## 1. Fast run:

### 1.1. For tar compressed app source files

```bash
# chmod +x run.sh
./run.sh tar
# Open in your browser: localhost:9080

# Cleaning
docker stop aquawebsite
docker rm aquawebsite
rm -rf aqua-tar
```

### 1.2. For NOT compressed app source files:

```bash
./run.sh plain
# Open in your browser: localhost:9080

# Cleaning
docker stop aquawebsite
docker rm aquawebsite
rm -rf aqua-not-tar
```


## 2. Step by step

### 2.1. For `tar compressed` app source files:

```bash
mkdir aqua-tar
cp Dockerfile-tar aqua-tar/Dockerfile
cd aqua-tar
# Download example app from: 
# https://www.tooplate.com/view/2138-aqua-nova
curl -L -O https://www.tooplate.com/zip-templates/2138_aqua_nova.zip
unzip 2138_aqua_nova.zip
rm 2138_aqua_nova.zip
cd 2138_aqua_nova
tar czvf aqua.tar.gz *
mv aqua.tar.gz ../
cd ..
rm -rf 2138_aqua_nova

docker build -t aqua_img .
docker images

# Run the Docker container in detached mode, name it 'aquawebsite', 
# and map port 9080 on your host to port 80 in the container
docker run -d --name aquawebsite -p 9080:80 aqua_img
docker ps -a

# open in the browser: localhost:9080

docker stop aquawebsite
docker rm aquawebsite


# ADD tag:
docker build -t aqua_img:V2 .
docker run -d --name aquawebsite -p 9080:80 aqua_img:V2

# open in the browser: localhost:9080

# Cleaning
docker stop aquawebsite
docker rm aquawebsite
rm -rf aqua-tar
```


### 2.2. For `NOT compressed` app source files:

```bash
mkdir aqua-not-tar
cp Dockerfile-not-tar aqua-not-tar/Dockerfile
cd aqua-not-tar
# Download example app from: 
# https://www.tooplate.com/view/2138-aqua-nova
curl -L -O https://www.tooplate.com/zip-templates/2138_aqua_nova.zip
unzip 2138_aqua_nova.zip
rm 2138_aqua_nova.zip
cd 2138_aqua_nova
mv * ../
cd ..
rm -rf 2138_aqua_nova

docker build -t aqua_img .
# docker images

docker run -d --name aquawebsite -p 9080:80 aqua_img
docker ps -a

# open in the browser: localhost:9080

docker stop aquawebsite
docker rm aquawebsite


# ADD tag:
docker build -t aqua_img:V3 .
docker run -d --name aquawebsite -p 9080:80 aqua_img:V3
docker ps -a

# open in teh browser: localhost:9080

# Cleaning
docker stop aquawebsite
docker rm aquawebsite
rm -rf aqua-not-tar
```