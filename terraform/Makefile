.PHONY: init plan apply

# Initialize Terraform
init:
	@echo "Initializing Terraform..."
	terraform init

# Plan the deployment
plan:
	@echo "Planning Terraform deployment..."
	terraform plan -var databricks_host="$(DATABRICKS_HOST)" \
	-var databricks_client_id="$(DATABRICKS_CLIENT_ID)" \
	-var databricks_client_secret="$(DATABRICKS_CLIENT_SECRET)" \
	-var lambda_exec_role_id="$(LAMBDA_ROLE_ID)" \
	-var lambda_exec_role_name="$(LAMBDA_ROLE_NAME)" \
	-var git_personal_access_token="$(GIT_PAT_TOKEN)" \
	-var aws_access_key_id="$(AWS_ACCESS_KEY_ID)" \
	-var aws_secret_access_key="$(AWS_SECRET_ACCESS_KEY)" \

# Apply the deployment
apply:
	@echo "Applying Terraform deployment..."
	terraform apply -var databricks_host="$(DATABRICKS_HOST)" \
	-var databricks_client_id="$(DATABRICKS_CLIENT_ID)" \
	-var databricks_client_secret="$(DATABRICKS_CLIENT_SECRET)"  \
	-var lambda_exec_role_id="$(LAMBDA_ROLE_ID)" \
	-var lambda_exec_role_name="$(LAMBDA_ROLE_NAME)" \
	-var git_personal_access_token="$(GIT_PAT_TOKEN)" \
	-var aws_access_key_id="$(AWS_ACCESS_KEY_ID)" \
	-var aws_secret_access_key="$(AWS_SECRET_ACCESS_KEY)" \
