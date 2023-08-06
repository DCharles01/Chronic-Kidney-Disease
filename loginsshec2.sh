#!/bin/bash

# Ask the user for RSA key, EC2 instance IP, and username
read -p "Enter the RSA key filename (e.g., rsa_key_name.pem): " RSA_KEY
read -p "Enter the EC2 instance public IP address: " PUBLIC_IP
read -p "Enter the username for SSH connection (e.g., ec2-user): " USERNAME

# Run the ssh command
ssh -i "$RSA_KEY" "$USERNAME"@"$PUBLIC_IP"
