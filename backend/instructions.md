# Local Installation instructions

## follow instructions to download docker here and make sure it is running
https://docs.docker.com/get-docker/

## Clone repository
git clone https://github.com/DCharles01/Chronic-Kidney-Disease.git

## cd into ckd folder if not already in it
cd Chronic-Kidney-Disease 

## build docker container
docker-compose up --build

## if you receive any errors, run the above line again and it should work

# Setting up EC2 Instance
Amazon EC2 (Elastic Compute Cloud) provides resizable compute capacity in the cloud. Follow these steps to create and run an EC2 instance:

## Sign in to Your AWS Account
If you don't have an AWS account, create one. Then, sign in to the AWS Management Console.

## Navigate to EC2 Dashboard
Once signed in, navigate to the EC2 Dashboard.

## create security groups in EC2 -> Networking & Security -> Security Groups
- Create the following inbound rules

–
	IPv4	HTTP	TCP	80	0.0.0.0/0	–

–
	IPv6	HTTP	TCP	80	::/0	–

–
	IPv4	Custom TCP	TCP	5000	0.0.0.0/0	–

–
	IPv4	SSH	TCP	22	0.0.0.0/0	–

–
	IPv4	Custom TCP	TCP	8501	0.0.0.0/0	–

–
	IPv4	HTTPS	TCP	443	0.0.0.0/0	–

- Create the following outbound rules

–
	IPv4	HTTP	TCP	80	0.0.0.0/0	–

–
	IPv6	HTTP	TCP	80	::/0	–

–
	IPv4	Custom TCP	TCP	5000	0.0.0.0/0	–

–
	IPv4	SSH	TCP	22	0.0.0.0/0	–

–
	IPv4	Custom TCP	TCP	8501	0.0.0.0/0	–

–
	IPv4	HTTPS	TCP	443	0.0.0.0/0	–

## Launch Instance
- Click on the "Instances" link in the left navigation pane.
- Click the "Launch Instances" button.
## Choose an Amazon Machine Image (AMI)
- Choose an AMI based on your requirements (e.g., Amazon Linux, Ubuntu, etc.).
- Click the "Select" button.
## Choose Instance Type
- Select an instance type based on your needs (e.g., t2.micro, m5.large, etc.).
- Click the "Next: Configure Instance Details" button.
## Configure Instance Details
- Configure the instance details like the number of instances, network settings, etc.
- Click the "Next: Add Storage" button.
## Add Storage (Optional)
- Configure the storage options based on your requirements.
- Click the "Next: Add Tags" button.
## Add Tags (Optional)
- Add tags to your instance for better organization (e.g., Name, Environment, etc.).
- Click the "Next: Configure Security Group" button.
## Configure Security Group
- Configure the security group to control inbound and outbound traffic.
- You can create a new security group or select an existing one.
- Click the "Review and Launch" button.
## Review and Launch
- Review your instance configuration.
- Click the "Launch" button.
##  Create a Key Pair
- Choose an existing key pair or create a new one.
- Download the private key file (.pem) – this is important for accessing your instance.
##  Launching Instances
- Click the "Launch Instances" button.
- A confirmation screen will appear.
## Access Your Instance
- Once your instance is running, note down its Public IP or DNS.
- Open a terminal or SSH client.
- Use the following command to connect to your instance:
bash
Copy code
ssh -i /path/to/your/key.pem ec2-user@your-instance-public-ip
Replace /path/to/your/key.pem with the actual path to your private key file and your-instance-public-ip with your instance's Public IP.

Following these steps will guide you through the process of creating and running an Amazon EC2 instance. Remember to manage your instances and their associated costs to avoid unnecessary charges.

Once you are in your ec2 instance, it's time to setup the environment
## Install Python
sudo yum install python3

## Install sqlite3
sudo yum install sqlite3

## Install Docker
sudo yum install docker -y
sudo usermod -aG docker $USER <!-- after this step press ctrl + d and log back into docker before starting it so the user can be added to the docker group-->
sudo systemctl start docker
- Use sudo systemctl enable docker to automatically start docker when you connect to your ec2 instance

## Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

## Install git
sudo yum install git

## Install pip
curl -O https://bootstrap.pypa.io/get-pip.py # download pip

python3 get-pip.py --user


## clone CKD repo
git clone https://github.com/DCharles01/Chronic-Kidney-Disease.git

## cd into ckd folder if not already in it
cd Chronic-Kidney-Disease 

## create network for both streamlit and flask docker containers to communicate with each other
docker network create flask_streamlit_conn

## build docker container
docker-compose up --build

## Connect to streamlit application via external URL