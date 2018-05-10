#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
$BASEDIR/../../upload_new_version_to_serverless_repo.sh battery_reports/sam/battery_level.yaml battery_reports/sam/battery_level_template.yaml
