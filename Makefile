BUCKET_NAME := cm-fujii.genki-deploy
STACK_NAME := Slack-Team-IoT-Reaction-Bot-Stack
PARAMETER_STORE_KEY := /Slack/Toekn/Team-IoT-Reaction-Bot


deploy:
	sam build  --use-container

	sam package \
		--output-template-file packaged.yaml \
		--s3-bucket $(BUCKET_NAME)

	sam deploy \
		--template-file packaged.yaml \
		--stack-name $(STACK_NAME) \
		--s3-bucket $(BUCKET_NAME) \
		--capabilities CAPABILITY_NAMED_IAM \
		--parameter-overrides SlackAppTokenKey=$(PARAMETER_STORE_KEY) \
		--no-fail-on-empty-changeset

get-output:
	aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[].Outputs'

delete-stack:
	aws cloudformation delete-stack \
		--stack-name $(STACK_NAME)

.PHONY: \
	deploy \
	get-output \
	delete-stack
