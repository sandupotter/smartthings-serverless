#!/usr/bin/env bash

function get_next_tag()
{
  latest_tag=`git describe --abbrev=0 --tags`
  tag_tokens=$(echo $latest_tag | tr "." "\n")

  next_tag=""
  current_token_index=1
  for token in $tag_tokens
  do
    if [ $current_token_index == "3" ]
    then
      token="$(($token+1))"
      next_tag=$next_tag$token
    else
      next_tag=$next_tag$token"."
    fi
    current_token_index="$(($current_token_index+1))"
  done
  echo $next_tag
}

BASEDIR=$(dirname "$0")
python $BASEDIR/setup.py ldist
SAM_TEMPLATE=$BASEDIR/$1
SAM_TEMPLATE_OUTPUT=$BASEDIR/$2
APPLICATION_ID=$3
SOURCE_URL=$4
NEXT_TAG=$(get_next_tag)
LATEST_TAG=`git describe --abbrev=0 --tags`

if [ $# -eq 3 ]
then
  SEMANTIC_VERSION=$NEXT_TAG
else
  SEMANTIC_VERSION=$5
fi

if [ $LATEST_TAG != $SEMANTIC_VERSION ]
then
  echo "Pushing new tag $SEMANTIC_VERSION ..."
  git tag $SEMANTIC_VERSION
  git push origin $SEMANTIC_VERSION
fi

AWS_SEMANTIC_VERSION=`echo $SEMANTIC_VERSION | cut -c 2-`

SOURCE_URL=`echo $SOURCE_URL | sed -e "s/version/$SEMANTIC_VERSION/g"`


aws cloudformation package --template-file $SAM_TEMPLATE --s3-bucket sandupotter-smart-things-serverless --output-template-file $SAM_TEMPLATE_OUTPUT
aws serverlessrepo create-application-version \
  --application-id $APPLICATION_ID \
  --semantic-version $AWS_SEMANTIC_VERSION \
  --source-code-url $SOURCE_URL \
  --template-body "file://"$SAM_TEMPLATE_OUTPUT

echo "Deployed app $APPLICATION_ID with version $AWS_SEMANTIC_VERSION"