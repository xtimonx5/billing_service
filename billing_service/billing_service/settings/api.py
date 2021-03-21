DEPOSIT_SCOPE = 'deposit'
TRANSFER_SCOPE = 'transfer'
ACCOUNT_SCOPE = 'account'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ]
}

OAUTH2_PROVIDER = {
    'SCOPES': {
        DEPOSIT_SCOPE: 'Deposit money to account',
        TRANSFER_SCOPE: 'Transfer money to another account',
        ACCOUNT_SCOPE: 'Check current balance & history',
    },
    'CLIENT_SECRET_GENERATOR_LENGTH': 20
}
