#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
python $BASEDIR/setup.py ldist
SAM_TEMPLATE=$BASEDIR/$1
SAM_TEMPLATE_OUTPUT=$BASEDIR/$2
aws cloudformation package --template-file $SAM_TEMPLATE --s3-bucket sandupotter-smart-things-serverless --output-template-file $SAM_TEMPLATE_OUTPUT