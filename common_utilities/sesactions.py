import boto3
from botocore.exceptions import ClientError
from common_utilities import setuplogger

logger = setuplogger.create_logger(__name__, stdout=True, level='DEBUG')


class SesActions:
    ses_client = boto3.client('ses')

    def send_email(self, from_address, to_addresses, subject, body_data, body_type='Text'):
        try:
            self.ses_client.send_email(
                Destination={
                    'ToAddresses': to_addresses
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        body_type: {
                            'Data': body_data
                        },
                    }
                },
                Source=from_address
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            if (e.response['Error']['Type']=='Sender' and e.response['Error']['Code']=='MessageRejected' and
                    'address is not verified' in e.response['Error']['Message']):
                self.setup_sender_email(from_address)
                logger.error('The from address %s needs to be verified first by SES. ' +
                             'Please check your email to verify it.'
                             % from_address)
                raise e
            else:
                raise e
        else:
            logger.debug('Sent email from %s to %s with subject: %s' % (from_address, to_addresses, subject))

    def setup_sender_email(self, from_address):
        from_address_setup_status = self.get_email_identity_status(from_address)
        if from_address_setup_status == 'NotExists':
            self.ses_client.verify_email_identity(
                EmailAddress=from_address
            )
            logger.debug('The email %s was setup for verification in SES' % from_address)

    def get_email_identity_status(self, from_address):
        response = self.ses_client.get_identity_dkim_attributes(
            Identities=[
                from_address
            ]
        )
        if from_address in response['DkimAttributes']:
            return response['DkimAttributes'][from_address]['DkimVerificationStatus']
        else:
            return 'NotExists'
