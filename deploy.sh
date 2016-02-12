#!/bin/bash

hugo

aws s3 sync public/ s3://codegoalie.com/ \
  --profile blog \
  --delete \
  --acl public-read 

aws cloudfront create-invalidation --distribution-id E2VC2R7NUNA9O8 \
  --path / \
  --profile blog
