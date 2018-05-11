# [SmartThings](https://www.smartthings.com/) Battery Level Report 

_Use case: Know the current temperature levels reported by SmartThings devices that have a temperature sensor_

Lambda that runs periodically (based on a configuration) and performs the following functions:
* reads the temperature reported devices that have a temperature sensor and are associated with the configured SmartThings account
* sends an email with 3 lists of devices: 
  * devices reporting a temperature lower or equal than the configured "Low Temperature Limit"
  * devices reporting a temperature higher or equal than the configured "High Temperature Limit"
  * the rest of the devices
* the lists are ordered based on the temperarture level
* the email is sent through the AWS Simple Email Service using the configured from and to addresses

**Prerequisites (needed before deploying the application)**

1. Generate a [SmartThings API Key](https://github.com/sandupotter/smartthings-serverless/blob/master/docs/smart_things_create_api_key/README.md)
2. [Setup](https://github.com/sandupotter/smartthings-serverless/blob/master/docs/ses_register_email/README.md) a FROM and a TO email address in AWS SES _(repeat the process twice for both the **from** and **to** email address)_. This needs to be done in the same region where the application will be deployed.