TF_DIR := ./backend/terraform/aws


up:
	docker-compose up
down:
	docker-compose down

tf-init:
	cd $(TF_DIR) && terraform init

tf-init-upgrade:
	cd $(TF_DIR) && terraform init -upgrade

tf-plan:
	cd $(TF_DIR) && terraform plan

tf-apply:
	cd $(TF_DIR) && terraform apply

tf-output-priv_key:
	cd $(TF_DIR) && terraform output private_key_pem

tf-output-ssh-key:
	cd $(TF_DIR) && terraform output private_key

tf-destroy:
	cd $(TF_DIR) && terraform destroy


