## Customer

# Create new a user(Customer).
curl -X POST -H "Content-Type: application/json" -d '{"email": "pablo@martinez.com", "phone":"3434343412", "username":"pablomartinez", "first_name":"pablo", "last_name": "martinez", "password": "Abcde-1234"}' http://localhost:8000/api_users/customer_register/

# Log in
curl -X POST -H "Content-Type: application/json" -d '{"email": "pablo@martinez.com", "password": "Abcde-1234"}' http://localhost:8000/api_users/customer_login/


## Worker

# Create new a user(Worker).
curl -X POST -H "Content-Type: application/json" -d '{"email": "laura@rodriguez.com", "phone":"123123123", "username":"laurarodriguez", "first_name":"laura", "last_name": "rodriguez", "password": "Abcde-1234"}' http://localhost:8000/api_users/worker_register/

# Log in
curl -X POST -H "Content-Type: application/json" -d '{"email": "laura@rodriguez.com", "password": "Abcde-1234"}' http://localhost:8000/api_users/worker_login/


## Require Token

# Test session (replace <token> for the retrieved token by the log-in endpoint)
curl -X POST -H "Authorization: Token <token>" http://localhost:8000/

# Log out (replace <token> for the retrieved token by the log-in endpoint)
curl -X POST -H "Authorization: Token <token>" http://localhost:8000/api_users/logout/