# API Endpoints

- POST `/api/authenticate/` - Authenticate a user and obtain a JWT token
- POST `/api/follow/<str:id>` - Follow a user.
- POST `/api/unfollow/<str:id>` - Unfollow a user.
- GET `/api/user/<str:username>/` - Get details of a user.
- POST `/api/post/add` - Add a new post.
- DELETE `/api/post/<str:pk>` - Delete a post.
- GET `/api/all_posts` - Get all posts of the authenticated user.
- GET `/api/get_post/<str:id>` - Get a particular post.
- POST /api/like/post/<str:id> - Like a post.
- POST /api/unlike/post/<str:id> - Unlike a post.
- POST /api/comment/post/<str:id> - Add a comment to a post.
