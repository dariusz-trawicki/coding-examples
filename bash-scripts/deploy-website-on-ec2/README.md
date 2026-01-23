# Bash script: Create EC2 and deploy website

### Run

```bash
chmod +x ./run.sh
USER_DATA_FILE=./user-data.sh USE_EIP=true MAP_PUBLIC_IP=false \
KEY_NAME=test-web-server-key \
bash ./run.sh
```

#### Test

**NOTE**: Wait about 2 minutes. [Apache is being installed on the EC2]

Open: http://PUBLIC_IP – the Apache welcome page will appear.

**SSH** connection:

```bash 
ssh -i ./test-web-server-key.pem ubuntu@PUBLIC_IP
sudo -i
fdisk -l
```

### Cleanup

```bash
chmod +x ./clean.sh
bash ./clean.sh
```

