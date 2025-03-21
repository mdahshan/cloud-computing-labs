# EC2 Example Linux Web Server with LAMP Stack

Define parameters

```bash
SECURITY_GROUP_ID="sg-xxx" # EC2SecurityGroup
VPC_ID="vpc-xxx"  # Work VPC
SUBNET_ID="subnet-xxx" # Work Public Subnet
AMI_ID="ami-0f403e3180720dd7e"  # Amazon Linux 2023
KEY_PAIR="vockey"
```

Define the startup script
```bash
read -r -d '' USER_DATA <<EOF
#!/bin/bash
# Install Apache Web Server and PHP
dnf install -y httpd wget php mariadb105-server

# Create a simple PHP file
echo '<?php phpinfo(); ?>' > /var/www/html/index.php

# Turn on web server
chkconfig httpd on
service httpd start
EOF
```

Update the security group to allow HTTP access


```bash
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0
```

Run EC2 Instance

```bash
aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type t2.micro \
    --key-name $KEY_PAIR \
    --security-group-ids $SECURITY_GROUP_ID \
    --subnet-id $SUBNET_ID \
    --user-data "$USER_DATA" \
```

With Name tag specified

```bash
aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type t2.micro \
    --key-name $KEY_PAIR \
    --security-group-ids $SECURITY_GROUP_ID \
    --subnet-id $SUBNET_ID \
    --user-data "$USER_DATA" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Web Server}]'
```
