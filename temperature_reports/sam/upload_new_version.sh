#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
$BASEDIR/../../upload_new_version_to_serverless_repo.sh temperature_reports/sam/temperature_level.yaml temperature_reports/sam/temperature_level_template.yaml
