#!/bin/bash

hugo

aws s3 cp public/ s3://codegoalie.com/ \
  --recursive \
  --profile blog \
  --acl public-read 
