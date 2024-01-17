#!/bin/bash

# Ask the user for RSA key, EC2 instance IP, and username
read -p "Enter the END POINT for RDS: " endpoint
read -p "Enter the username for RDS: " username
read -p "Enter the database_name for RDS: " database # streamlitdb

# run chmod 0400 pem_name.pem if any issues

# Run the psql command
psql -h "$endpoint" -U "$username" -d "$database" -W

