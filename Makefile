.PHONY: deploy build push invalidate
deploy: build push invalidate

build:
	hugo

push:
	aws s3 sync public/ s3://codegoalie.com/ \
		--profile blog \
		--delete \
		--acl public-read 

invalidate: push
	aws cloudfront create-invalidation --distribution-id E2VC2R7NUNA9O8 \
		--path / \
		--profile blog
