# Simple Inventory Management System (SIMS)

Tech Stacks: Django, SQLite

URL: https://sims.juwaini.com/

Credentials:
------------

For 'Guest' user: guest:abcdwxyz

For 'Admin' user: juwaini:abcdwxyz

1. Endpoint `/api/inventory`
2. Endpoint `/api/inventory/<int:pk>`
3. Endpoints `/api/add-inventory`, `/api/delete-inventory`, `/api/update-inventory`
4. Can be run by using command: `./manage.py populate_data`, thanks to Faker library. Bonus: automatically created user 'guest' and 'juwaini' with 'Guest' and 'Admin' role respectively.
5. Endpoint `/inventory`: using datatables, so mechanism to filter, sort and paginate are automatically done. One button to add product, except if you're a 'Guest'.
6. Endpoint `inventory/<int:pk` with show details of product with pk. Button to update and delete. Minus: no static image of the product

[MANDATORY MID-LEVEL] - Using battery-included django permissions, all the roles have been created & assigned at #4.

[MANDATORY SENIOR]
1. Using django admin (accessible by 'juwaini' account) at `/admin`, you can create new role (Group) and re-assign permissions. You can view your own permission in index (endpoint: `/`) page.
2. Created a few test cases for permutations of roles vs actions, but test cases of `a` and `b` are done.
