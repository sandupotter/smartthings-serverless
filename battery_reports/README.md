# [SmartThings](https://www.smartthings.com/) Battery Level Report 

Lambda that runs periodically (based on a configuration) and performs the following functions:
* reads the battery level for all the battery enabled devices associated with the configured SmartThings account
* sends an email with 2 lists of devices: 
  * devices with a battery level lower than the configured "Minimum Acceptable Battery Level"
  * the rest of the devices
* the lists are ordered based on the remaining battery level
* the email is sent through the AWS Simple Email Service using the configured from and to addresses

**Prerequisites (needed before deploying the application)**

1. Generate a [SmartThings API Key](https://github.com/sandupotter/smartthings-serverless/blob/master/docs/smart_things_create_api_key/README.md)
2. [Setup](https://github.com/sandupotter/smartthings-serverless/blob/master/docs/ses_register_email/README.md) a FROM and a TO email address in AWS SES _(repeat the process twice for both the **from** and **to** email address)_. This needs to be done in the same region where the application will be deployed.