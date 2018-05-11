#!/usr/bin/env bash
APPLICATION_ID=$1
ACCOUNT_ID=$2
aws serverlessrepo put-application-policy --application-id $APPLICATION_ID --statements Actions=Deploy,Principals=$ACCOUNT_ID,StatementId="Statement"$ACCOUNT_ID