# EC2 Example Linux Web Server with LAMP Stack

Define parameters

```bash
SECURITY_GROUP_ID="sg-xxx" # EC2SecurityGroup
VPC_ID="vpc-xxx"  # Work VPC
SUBNET_ID="subnet-xxx" # Work Public Subnet
AMI_ID="ami-0f9c44e98edf38a2b"  # Windows Server 2022 Base
KEY_PAIR="vockey"
```

Update the security group to allow RDP access

```bash
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 3389 \
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
    --user-data "$USER_DATA"
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
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Windows Server}]'
```

Get Instance ID

```bash
aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=Windows Server" \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text
```

