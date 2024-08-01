.PHONY: all clean zip apply_terraform git_push

all: zip apply_terraform git_push

# Step to zip the lambda functions
zip: zoopla_publishing_service.zip raw_listings_s3_event_lambda.zip

zoopla_publishing_service.zip:
	cd lambda_functions/zoopla_publishing_service && zip -r ../../zoopla_publishing_service.zip lambda_function.py

raw_listings_s3_event_lambda.zip:
	cd lambda_functions/raw_listings_s3_event_lambda && zip -r ../../raw_listings_s3_event_lambda.zip lambda_function.py

# Step to apply the terraform
apply_terraform:
	cd terraform && make all

clean:
	rm -f zoopla_publishing_service.zip raw_listings_s3_event_lambda.zip

git_push:
	git add --all .; git commit -am "update"; git push
