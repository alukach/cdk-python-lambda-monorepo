.PHONEY: lint format diff deploy destroy

lint:
	pipenv run flake8 lambdas/ cdk/ layers/ cdk.py
	pipenv run isort --check-only --profile black lambdas/ cdk/ layers/ cdk.py
	pipenv run black --check --diff lambdas/ cdk/ layers/ cdk.py

format:
	pipenv run isort --profile black lambdas/ cdk/ layers/ cdk.py
	pipenv run black lambdas/ cdk/ layers/ cdk.py

diff:
	pipenv run npx cdk diff || true

deploy:
	pipenv run npx cdk deploy --require-approval never

destroy:
	pipenv run npx cdk destroy --force
