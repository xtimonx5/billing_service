# Billing Service

Service provides 4 urls to
* Register (`/api/register/`) to Register new user and account
* Deposit (`/api/deposit/`) to Deposit $ to your account
* Transfer (`/api/transfer/`) to transfer $ to another user
* Account (`/api/account/`) to check your balance


Also, there are a few urls, provided by oauth2 auth backend
https://github.com/jazzband/django-oauth-toolkit


### API documentation
#### Register endpoint
url: `/api/register/`
method: POST

permissions: Allow any
http body example:
```
{
    "username": "test_user",
    "email": "test@test.com",
    "password": "1234567890qwerty"
}
```

| Field name | Field type | Limitations                                         |
|------------|------------|-----------------------------------------------------|
| username   | char       |                                                     |
| password   | char       | * Longer than 8 symbols * Contains digits & letters |
| email      | char       | Valid email                                         |

Example with curl
```
curl -i -X POST -H "Content-Type: application/json" http://0.0.0.0:8000/api/register/ -d '{"username": "fefe", "password": "qa1q1we23ew1", "email": "qwe@qweqw.com"}'
```

Response example
```
{
    "username":"fefe",
    "email":"qwe@qweqw.com",
    "client_id":"8FL6vq5pT8R5WuwlJ0sSPKkNPXihIj1VB43XTsPH",
    "client_secret":"GVTklxE4BvTo0juezEMC",
    "b64header":"OEZMNnZxNXBUOFI1V3V3bEowc1NQS2tOUFhpaElqMVZCNDNYVHNQSDpHVlRrbHhFNEJ2VG8wanVlekVNQw=="
}
```


#### Getting access token
To authorize the user, it is required to send POST request to URL http://0.0.0.0:8000/api/oauth2/token/ using client_id, base64header, password from registration step


HTTP body

| Field name | Field type | Details                                             |
|------------|------------|-----------------------------------------------------|
| grant_type | char       | in current version `password` value only            |
| scope      | char       | List of scopes separated by space                   |
| username   | char       | Username                                            |
| password   | char       | Your password                                       |

Headers:
| Header name | Value                                                |
|-------------|------------------------------------------------------|
| grant_type  | Basic #{Your b64header from registration step}       |


Available scopes
| Scope name   | Description                                          |
|--------------|------------------------------------------------------|
| deposit      | Deposit money to account                             |
| transfer     | Transfer money to another account                    |
| account      | Check current balance & history                      |

Example: 
```
curl -H 'Authorization: Basic OEZMNnZxNXBUOFI1V3V3bEowc1NQS2tOUFhpaElqMVZCNDNYVHNQSDpHVlRrbHhFNEJ2VG8wanVlekVNQw==' -X POST 
http://0.0.0.0:8000/api/oauth2/token/ -d 'grant_type=password&scope=account transfer&username=fefe&password=qa1q1we23ew1'
```

Response example

```
{
    "access_token": "jlRRgXGKKAcO1ByrvH6VkpraiPu9Uv", 
    "expires_in": 36000, 
    "token_type": "Bearer", 
    "scope": "account transfer", 
    "refresh_token": "Kt4NtfZGnT0sdU47dDOkfXjGgf2GOc"
}
```

`access_token` is required to interact with other endpoints. 



#### Deposit endpoint
url: `/api/deposit/`
method: POST

permissions: Access token with `deposit` scope
http body example:
```
{
    "amount": "10.00",
}
```

| Field name | Field type | Limitations                                         |
|------------|------------|-----------------------------------------------------|
| amount     | decimal    | >=0.01                                              |

Example with curl
```
curl -i -X POST -H "Authorization: Bearer MbhDUqjtL5SXgj2Wtmu9CArT04bZff" -H "Content-Type: application/json" http://0.0.0.0:8000/api/deposit/ -d '{"amount": "55.5"}'
```


#### Transfer endpoint
url: `/api/transfer/`
method: POST

permissions: Access token with `transfer` scope
http body example:
```
{
    "amount": "0.2", 
    "recipient_username":"qeqweqw"
}
```

| Field name             | Field type | Limitations                                         |
|------------------------|------------|-----------------------------------------------------|
| amount                 | decimal    | >=0.01                                              |
| recipient_username     | char       | existent username                                   |

Example with curl
```
 curl -i -X POST -H "Authorization: Bearer MbhDUqjtL5SXgj2Wtmu9CArT04bZff" -H "Content-Type: application/json" http://0.0.0.0:8000/api/transfer/ -d '{"amount": "0.2", "recipient_username":"qeqweqw"}'
```



#### Account endpoint
url: `/api/account/`
method: GET

permissions: Access token with `account` scope
Curl example
```
curl -i -H "Authorization: Bearer MbhDUqjtL5SXgj2Wtmu9CArT04bZff" http://0.0.0.0:8000/api/account/
```
Response example:
```
{
  "balance": "1165.35",
  "username": "qwe134",
  "history": [
    {
      "date": "2021-03-21T15:36:11.999291",
      "operation_type": "transfer",
      "amount": "-0.20"
    },
    {
      "date": "2021-03-21T14:00:56.737084",
      "operation_type": "deposit",
      "amount": "55.50"
    },
    {
      "date": "2021-03-21T14:00:12.588598",
      "operation_type": "deposit",
      "amount": "55.50"
    }
  ]
}
```