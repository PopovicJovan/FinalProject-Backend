# FinalProject-Backend

### User registration
Endpoint for user registration is **/register/**. That endpoint only allows POST method!
When you wanna create(register) user you have to send **username,first_name,last_name,password**. All of them are Charfields.
**Max length:**
**username** must be less than 32 char, **first_name** and **last_name** must be less than 16 char and **password** must be less than 128 char.

### User login/logout
Endpoint for user login or logout is **/login/** . You will pass **username** and **password** and if user with that **username** and **password** exists it will return you users token otherwise it returns error message!
When user tries to logout you send delete request on endpoint **/login/${tokenvalue}** and token will be deleted.
Token validation:
You can send get request with token on endpoint **/token/** if you wanna know if the token is valid or not!

### Users
You can access to list of all users that are registered.
Endpoint for that is **/Users/** .You will be able to get it only if you send token of superuser!**(I have already made it , remember that superuser token is
8ce37f7be9f53f36bc8867e873aa9725b34cfdc9
and username and password are admin, admin!)**
When you wanna get informations of specific user just add **/${id}/** after **/Users/**. You will be able to get it only if you send token of superuser or token of user you want to access!
If you wanna update informations of user send put/patch request on **/Users/${id}/** with token of that user or superuser!
If you wanna delete user , send delete request with token of that user or token of superuser on **/Users/${id}/** !
User attributes are described in user registration part of documentation!
You can filter users by username . In endpoint just add

**?username=${value}/**

### Blogs
You can access to all blogs from site on endpoint /Blogs/. In your request you have to pass token to prove that you are logged in. If you wanna access to specific blog just add /${id}/ on your endpoint.
When you send delete or put request you can only do it on your blogs unless you are superuser.
One blog has **title**, **content** , **author**, **id**, **average_rate**, **date_created**, **date_updated**. You cannot send or change **id**, **average_rate**, **date_created** and **date_updated**.
When you pass values , pass author as id from user base, pass content and title as string where content cannot be over 15000 char and title cannot be over 32 char!
When you do update/create request send only title or/and content!
You can filter blogs by average_rate, author, title . In endpoint just add

**?username=${value}&author=${value}&title=${value}**

### Recension
You can access to all recensions by endpoint **/Recension/**.
If you wanna access to specific recension just add **/${id}/**.
Whatever you do , you have to send token value!
You can delete and update only yours recensions unless you are superuser.
Recension has 4 attributes **id**, **author**, **rate**, **blog**.
You will pass value of author as integer that is id of author from user model. rate is integer from 1 to 5 and value of blog is integer id of blog from blog base.
If you do update of recension you have to send id of recension as 'id' and rate.
If you do post request you have to send rate and id of blog as 'blog'.
You can filter blogs by rate, author, blog . In endpoint just add

**?rate=${value}&author=${value}&blog=${value}**

### Comments
You can access to all comments by endpoint **/Comments/**.
If you wanna access to specific recension just add **/${id}/**.
You can delete and update only yours recensions unless you are superuser.
Comment has 4 attributes **id, author, content, blog**.
You will pass value of author as integer that is id of author from user model, value of blog is id of blog from blog base and content is string that cannot be over 1020 char!
When you do post request you have to send content and blog id as 'id'.
When you do update request you have to send id of comment and content.
Whatever you do , you have to send token value!
You can filter comments by author, blog . In endpoint just add

**?author=${value}&blog=${value}/**



