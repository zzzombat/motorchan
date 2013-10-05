Data
====

Objects
-------

::

   User: {
      username: str,
      password: str,

   }


   Board: {
      _id: MongoId,
      slug: str,
      name: str,
      post_max_id: int,

   }


   Thread: {
      _id: MongoId,
      no: int,
      op: Post,
      replies: [Post, Post, ...]

   }

   Post: {
      no: int,
      name: str,
      email: str,
      board_id: int,
      is_sage: bool,
      parent_id: int,
      body: str,
      image_url: str,
      date: MongoDate,

   }

Collections
-----------

   users: [User, User, ...]
   threads: [Thread, Thread, ...]

