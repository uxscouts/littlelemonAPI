super user
------------------------
user: admin
email: admin@admin.com
pass: ToothTown@2
-------------------------

user: manager_user
pass: ToothTown@3

-------------------------

user: delivery_user
pass: ToothTown@4

-------------------------

user: customer_user
pass: ToothTown@5
auth_token: "18083a01f014347c6f5375ec8b6d57e646d67e8a"

curl -X GET http://127.0.0.1:8000 -H "Authorization: Token 18083a01f014347c6f5375ec8b6d57e646d67e8a"

curl -X GET http://127.0.0.1:8000/api/cart/menu-items/ -H "Authorization: Token 18083a01f014347c6f5375ec8b6d57e646d67e8a"



