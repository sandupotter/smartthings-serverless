#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
#python $BASEDIR/setup.py ldist
SAM_TEMPLATE=$BASEDIR/$1
SAM_TEMPLATE_OUTPUT=$BASEDIR/$2
#aws cloudformation package --template-file $SAM_TEMPLATE --s3-bucket sandupotter-smart-things-serverless --output-template-file $SAM_TEMPLATE_OUTPUT
sample_template_output_one_line=`tr -d '\n' < $SAM_TEMPLATE_OUTPUT`
aws serverlessrepo create-application-version \
  --application-id arn:aws:serverlessrepo:us-west-2:180953841693:applications/smart-things-temperature-level-report \
  --semantic-version 1.0.1 \
  --source-code-url https://github.com/sandupotter/smartthing-serverless \
  --template-body "file://"$SAM_TEMPLATE_OUTPUT
