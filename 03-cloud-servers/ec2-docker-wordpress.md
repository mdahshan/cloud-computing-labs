Define parameters

```bash
SECURITY_GROUP_ID="sg-xxx" # EC2SecurityGroup
VPC_ID="vpc-xxx"  # Work VPC
SUBNET_ID="subnet-xxx" # Work Public Subnet
AMI_ID="ami-0f403e3180720dd7e"  # Amazon Linux 2023
KEY_PAIR="vockey"
DB_PASSWORD=your_mariadb_password
```

Update the security group to allow HTTP access

```bash
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0
```

Update the security group to allow HTTPS access

```bash
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0
```

Run EC2 instance

```bash
aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type t2.micro \
    --key-name $KEY_PAIR \
    --security-group-ids $SECURITY_GROUP_ID \
    --subnet-id $SUBNET_ID \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WordPress Server}]'
```


Install Docker

```bash
sudo dnf -y install docker
sudo service docker start
sudo docker ps
```

Run the WordPress Docker application

```bash
sudo docker pull wordpress
```

Run the MariaDB database container, creating a database "wordpress"

```bash
sudo docker pull mariadb

sudo docker run -d --name mymariadb -e MYSQL_ROOT_PASSWORD=$DB_PASSWORD -e MYSQL_DATABASE=wordpress mariadb
```

Finally, run the Docker container, connecting to MariaDB database using host name "mysql"

```bash
sudo docker run -d --name mywordpress -p 80:80 -p 443:443 --link mymariadb:mysql wordpress
```

Alternatively, install everything at startup

Define the startup script
```bash
read -r -d '' USER_DATA <<EOF
#!/bin/bash
dnf -y install docker
service docker start
docker pull wordpress
docker pull mariadb
docker run -d --name mymariadb -e MYSQL_ROOT_PASSWORD=$DB_PASSWORD -e MYSQL_DATABASE=wordpress mariadb
docker run -d --name mywordpress -p 80:80 -p 443:443 --link mymariadb:mysql wordpress
EOF
```

Then, run the EC2 instance

```bash
aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type t2.micro \
    --key-name $KEY_PAIR \
    --security-group-ids $SECURITY_GROUP_ID \
    --subnet-id $SUBNET_ID \
    --user-data "$USER_DATA" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WordPress Server}]'
```

