# API Format

- `pending` will be replaced by the url after it is finished. 

- All the return results have  `reason` which includes the error message. 

- ` "email" : "string not nul(need check value as "%@%")"`  

  --`email` is the name of element. 

  --`string` is the type of this element. (For the bool type, **1** for true and **0** for false)

  -- If the`not null` is behind the type, this means that the backend program will check this element is 		            null or not. The **F** would be return if it is null.

  -- Everything between the `()` is the explaination of this element. 

- `http status code 200/404/400` 

- `date` format is `YYYY-MM-DD`

## Home page

#### Get:  http://13.210.33.67:5000/Home_page

Argument:

```json
{
    "page_number": "int not null",
    "token" : "string"
}
```

Return result:

```json
{
    "items": [
        {
            "name": "string",
            "rating": "double",
            "rating number": "int",
            "price": "int",
            "image": "url",
            
        }
        (..up to 6 itmes)
    ],
    "exist_next_pages": "bool (if no, do not show the next button)",
    "reason" : "used for failure information",
}

http status code: 200/400/404(occurs when there is no more items, should not happen)
```



## sign in

#### Post: http://13.210.33.67:5000/Login

Arguments:

```json
{
    "email" : "string not null",
    "password" : "string not null"
}
```

Return:

```json
{
    "reason" : "used for failure information",
    "user_id": "int"
    "photo" : "url",
    "unread_message" : "bool (show the notification if it is 1)",
    "unread_trip" : "bool (show the notification if it is 1)",
    "token" : "string (default expiration time is 10 minutes)" ,
    "verified" : "bool (if not, cannot post or book)"
}
```




## sign up

#### Post: http://13.210.33.67:5000/Register

Arguments:

```json
{
    "email" : "string not null(need check value as "%@%")",
    "password" : "string(need to encrypt, not null)",
    "name" : "string, not null",
    "gender" : "M or F (only this two values are valid)",
    "date_of_birth" : "date format",
    "self_description" : "long string",
    "phone" : "string",
    "photo" : "url"
}
```

Return result:

```json
{
    "reason" : "used for failure information"
}

http status code: 200/403(when duplicate)/400("not null" attributes do not exist)/404
```



## Edit Profile

#### Get: http://13.210.33.67:5000/Edit-profile

Arguments: 

```json
{
    "token" : "string"
}
```

Return:

```json
{
    "name" : "string",
    "gender" : "M or F (only this two values are valid)",
    "phone" : "string",
    "date_of_birth" : "date",
    "self_description" : "string",
    "photo" : "url",
    "reason" : "used for failure information",
}

htpp status code: 200/400/404
```



####Put: http://13.210.33.67:5000/Edit-profile

Arguments: 

```json
{
    "token" : "string",
    "name" : "string (not null)",
    "gender" : "M or F (not null)",
    "phone" : "string",
    "date_of_birth" : "date",
    "self_description" : "string",
    "photo" : "url"
}
```

Result:

```json
{
    "reason" : "used for failure information"
}

http status code: 200/400/404
```



## Search

#### Get: http://13.210.33.67:5000/Search

Argument:

```json
{
    "key_word" : "string not null",
    "start_date" : "date",
    "end_date" : "date",
    "rating" : "int[a][b] (rating between a and b)",
    "price" : "int [a][b] (price between a and b)",
    "type" :  "string (apartment, house....)",
    
    "page_number": "int not null"
    (...can add more filter conditions)
}
```

Return type:

```json
{
    "items": [
        {
            "id" : "int",
            "name": "string",
            "rating": "double",
            "rating_number": "int",
            "price": "int",
            "image": "url",
            
        }
        (..up to 10 itmes)
    ],
    "total_pages": "int",
    "current_page": "int",
    "reason" : "used for failure information"
}

http status code: 200/400/404(occurs when there is no more items, should not happen)
```



## Post Item

#### Post:  http://13.210.33.67:5000/Item_operation

Arguments:

```json
{
 	"token" : "string not null",
    "user_id" : "int not null",
    
    "house_name" : "string not null",
    "description" : "string",
    "country" : "string not null",
    "city" : "string not null",
    "suburb" : "string not null",
    "address" : "string not null",
    "type" : "string",
    "price" : "float not null",
    "postcode" : "int not null",
   	
    "room_arrangement" : "string[a][b] (room a includes [b bed type, ...] )",
    "common_space" : "string[b] (same as previous b)",
    "bath_number" : "string not null",
    "max_people" : "string not null",
    "amenities" : "string[] not null",
    "photos" : "url[] not null"
}
```

Result:

```json
{
    "reason" : "used for failure information"
}

http status code: 200/400(when post duplicate item)/404
```



## Update Item

#### Put:  http://13.210.33.67:5000/Item_operation

Arguments: (same as item post but needs item id)

```json
{
 	"token" : "string not null",
    
    "host_id" : "int",
    "house_id" : "int", 
    "house_name" : "string",
    "description" : "string",
    "country" : "string",
    "city" : "string",
    "suburbs" : "string",
    "address" : "string",
    "type" : "string",
    "price" : "int",
   	
    "room_arrangement" : "string[a][b] (room a includes [b bed type, ...] )",
    "common_space" : "string[b] (same as previous b)",
    "bath_number" : "int",
    "max_people" : "int",
    "amenities" : "string[]",
    "photos" : "url[] not null"
}
```

Result:

```json
{
    "reason" : "used for failure information"
}

http status code: 200/400/404
```



##Click Item 

#### Get:  http://13.210.33.67:5000/Item_operation

Arguments:

```json
{
    "token" : "string",
    "house_id" : "int (not null)"
}
```

Return:

```json
{
    "hoster_id" : "int",
    "hoster_name" : "string",
    "hoster_photo" : "url", 
    
    "house_id" : "int",
    "house_name" : "string",
    "house_photo" : "url",
    "description" : "string",
    "country" : "string",
    "city" : "string",
    "suburb" : "string",
    "address" : "string",
    "type" : "string",
    "price" : "int",
    "accuracy_rating" : "double",
    "communication_rating" : "double",
    "cleanliness_rating" : "double",
    "loaction_rating" : "double",
    "check_in_rating" : "double",
    "value_rating" : "double",
    "post_code" : "int",
   	
    "room_arrangement" : "string[a][b] (room a includes [b bed type, ...] )",
    "common_space" : "string[b] (same as previous b)",
    "bath_number" : "int",
    "max_people" : "int",
    "amenities" : "string[]"
}

http status code: 200/400/404
```



## Get host item

#### Get:  http://13.210.33.67:5000/Item_specific_user

Arguments:

```json
{
    "token" : "string (not null)",
    "user_id" : "int (not null)"
}
```

Return:

```json
{
    "items" : [
        {
            "hoster_id" : "int",
            "hoster_name" : "string",
            "hoster_photo" : "url", 

            "house_id" : "int",
            "house_name" : "string",
            "house_photo" : "url",
            "description" : "string",
            "country" : "string",
            "city" : "string",
            "suburb" : "string",
            "address" : "string",
            "type" : "string",
            "price" : "int",
            "accuracy_rating" : "double",
            "communication_rating" : "double",
            "cleanliness_rating" : "double",
            "loaction_rating" : "double",
            "check_in_rating" : "double",
            "value_rating" : "double",

            "room_arrangement" : "string[a][b] (room a includes [b bed type, ...] )",
            "common_space" : "string[b] (same as previous b)",
            "bath_number" : "int",
            "max_people" : "int",
            "amenities" : "string[]"
		}
		(...)
    ]
}

http status code: 200/400/404
```







##Delete Item

#### Delete: http://13.210.33.67:5000/Item_operation

Arguments: 

```json
{
    "token" : "string not null",
    "house_id" : "int (not null)"
}
```

Return:

```json
{
    "reason" : "used for failure information"
}

http status code: 200/400/404
```



## Message

#### Get: http://13.210.33.67:5000/Message/preview (for preview)

Arguments:

```json
{
    "token" : "string not null",
    "user_id" : "int not null"
}
```

Result:

```json
{
    "message" : [
        {
            "last_message" : "string",
            "user_id" : "int",
            "receiver_id" : "int",
            "sender_id" : "int (who sends this last message)",
            "read_or_not" : "bool"
        }
        (... all messages)
    ]
}

http status code 200/400/404
```



#### Get: http://13.210.33.67:5000/Message/detail    (for detail)

Arguments:

```json
{
    "token" : "string not null",
    "user_id" : "int not null (same as id in token)",
    "receiver_id" : "int not null"
}
```



Result:

 ```json
{
    "message" : [
        {
            "content" : "string",
            "sender" : "int (who send this message, id would be one of the user and 							sender)",
            "date" : "timestamp"
        },
        ...(all the message)
    ],
    "user" : {
        "id" : "int",
        "photo" : "url",
        "name" : "string"
    },
    "sender" : {
        "id" : "int",
        "photo" : "url",
        "name" : "string"
    }
}

http status code 200/400/404
 ```



#### Post:  http://13.210.33.67:5000/Message/post    (for send message)

Arguments: 

```json
{
    "token" : "int",
    "user_id" : "int",
    "receive_id" : "int",
    "message_content" : "string",
    "date" : "date"
}
```

Result: 

```json
{
   	"reason" : "used for failure information"
}

http status code 200/400/404
```



## Unavailable Date

#### Get:  http://13.210.33.67:5000/Unavailable_date

Arguments:

```json
{
    "house_id" : "int not null",
    "start_date" : "date" 
}
```

Result: 

```json
{
    "reason" : "used for failure information",
    "unavailable" : "date[]"
}

http status code 200/400/404
```



## Booking 

#### Post: http://13.210.33.67:5000/Book

Arguments:

```json
{
    "token" : "string not null",
    "item_id" : "int not null",
    "host_id" : "int not null",
    "user_id" : "int not null",
    "date" : "date",
    "start_date" : "date not null",
    "end_date" : "date not null",
    "comment" : "string"
}
```

Result:

```json
{
    "reason" : "used for failure information"
}
(back end need to update unread trip to host in user_information db)

http status code 200/400/404
```



## Trips

####Get: http://13.210.33.67:5000/Trip

Arguments:

```json
{
    "token" : "string not null",
    "user_id" : "id not null"
}
```

Result:

```json
{
    "transaction" : [
        {
            "trip_or_not" : "bool (1 for trip, 0 for reservation)"
            "status" : "accepted/declined/completed/pending
            			(add accept/decline buttons when it is reservation)"
            
            "transaction_id" : "int"
            "house_id" : "int",
            "house_name" : "string",
            
            "user_id" : "int"
            "user_name" : "string",
            "user_photo" : "url",
            
            "start_date" : "date",
            "end_date" : "date",
            "review_or_not" : "bool"
    	} ...
    ],
    "reason" : "used for failure information"
}

(back end need to update unread trip to host in user_information db.
 check if the status is accept and end_date < datetime.now(), change status to complete)
```



## Confirm Transaction: Host

#### Post:http://13.210.33.67:5000/Confirm/Host

Arguments:

```json
{
    "token" : "string not null",
    "host_id" : "int not null",
    "transaction_id" : "int not null",
    "status" : "Accept/decline not null"
}
```

Result:

```json
{
    "reason" : "used for failure information"
}
(back end need to chage transacation status, 
 if it is accept, insert all unavailable date to the db.
update unread trip to the user who book this item)
```



## Confirm Transaction: User

#### Post:http://13.210.33.67:5000/Confirm/User

Arguments:

```json
{
    "token" : "string not null",
    "user_id" : "int",
    "transaction_id" : "int not null",
    "status" : "cancel"
}
```

Result:

```json
{
     "reason" : "used for failure information"
}
(need to check status: the completed transactions can not be changed,
change host unread trip,
change transaction status,
if it is accepted, delete all the date in unavailable_date).
```



## Post informtaion

####Post:  http://13.210.33.67:5000/Posts

Arguments:

```json
{
    "token" : "string not null",
    "user_id" : "int not null",
    "country" : "string",
    "city" : "string",
    "suburb" : "string",
    "post_date" : "date not null",
    "start_date" : "date not null",
    "end_date" : "date not null",
    "price_start" : "double not null",
    "price_end" : "double not null"
    "people_number" : "int not null",
    "comment" : "string"
}
```

Result:

```json
{
     "reason" : "used for failure information"
}
(put information to Post table)
```

#### Get:  http://13.210.33.67:5000/Post (all post information in date decreasing order)

Arguments: (do not need)

Result:

```json
{
    "posts" : [
        {
            "post_id" : "int",
            "user_id" : "int not null",
            "user_name" : "string",
            "user_photo" : "url",
            
            "country" : "string",
            "city" : "string",
            "suburb" : "string",
            "start_date" : "date",
            "end_date" : "date",
            "post_date" : "date",
            "price_start" : "double not null",
            "price_end" : "double not null"
            "people_number" : "int not null",
            "comment" : "string"
        }
        (...)
    ],
    "reason" : "used for failure information"
}
```



#### Get:  http://13.210.33.67:5000/Post_specific

Arguments:

```json
{
    "token" : "string not null",
    "user_id" : "int not null"
}
```

Result:

```json
{
    "Post" : [
        {
            "post_id" : "int",
            "user_id" : "int not null",
            "country" : "string",
            "city" : "string",
            "suburb" : "string",
            "start_date" : "date not null",
            "end_date" : "date not null",
            "post_date" : "date not null",
            "price_start" : "double not null",
            "price_end" : "double not null"
            "people_number" : "int not null",
            "comment" : "string",
		}
        (...)
    ],
    "reason" : "used for failure information"
}
```



#### Delete:  http://13.210.33.67:5000/Post

Arguments:

```json
{
    "token" : "string not null",
    "user_id" : "int not null",
    "post_id" : "int not null"
}
```

Result:

```json
{
    "reason" : "used for failure information"
}
```



#### Update:  http://13.210.33.67:5000/Post

Arguments:

```json
{
    "token" : "string not null",
    "user_id" : "int not null",
    "post_id" : "int not null",
    "country" : "string",
    "city" : "string",
    "suburb" : "string",
    "start_date" : "date not null",
    "end_date" : "date not null",
    "post_date" : "date not null",
    "price_start" : "double not null",
    "price_end" : "double not null"
    "people_number" : "int not null",
    "comment" : "string"
}
```

Result:

```json
{
     "reason" : "used for failure information"
}
(put information to Post table)
```

#### 

## Review

#### Get:http://13.210.33.67:5000/Review

Arguments:

```json
{
   	"itme_id" : "int not null"
}
```

Result:

```json
{
    "review" : [
        {
            "user_id" : "int",
            "user_photo" : "url",
            "date" : "date",
            "comment" : "string",
            "accuracy" : "int",
            "communication" : "int",
            "cleanliness" : "int",
            "location" : "int",
            "check_in" : "int",
            "value" : "int"
        }
		(...)    
    ],
	"result" : "used for failure information"
}
```



####Post:

Argument:

```json
{
    "token" : "string not null",
    "user_id" : "int not null",
    "transaction_id" : "int not null",
    "date" : "date",
    
    "comment" : "string",
    "accuracy" : "int",
    "communication" : "int",
    "cleanliness" : "int",
    "location" : "int",
    "check_in" : "int",
    "value" : "int"
    
}
```

Result:

```json
{
    "result" : "used for failure information"
}
```



##Search_Post

#### Get: http://13.210.33.67:5000/SearchPost

Argument:

```json
{
    "key_word" : "string not null",
    "start_date" : "date",
    "end_date" : "date",
    "price" : "int [a][b] (price between a and b)",
    
    "page_number": "int not null"
    (...can add more filter conditions)
}
```

Return type:

```json
{
     "posts" : [
        {
            "post_id" : "int",
            "user_id" : "int not null",
            "user_name" : "string",
            "user_photo" : "url",
            
            "country" : "string",
            "city" : "string",
            "suburb" : "string",
            "start_date" : "date",
            "end_date" : "date",
            "post_date" : "date",
            "price_start" : "double not null",
            "price_end" : "double not null"
            "people_number" : "int not null",
            "comment" : "string"
        }
        (...)
    ],
    "total_pages": "int",
    "current_page": "int",
    "reason" : "used for failure information"
}

http status code: 200/400/404(occurs when there is no more items, should not happen)
```



## User_information

#### Get: http://13.210.33.67:5000/User_information

Arguments:

```json
{
    "user_id" : "int not null"
}
```

Results:

```json
{
    "name" : "string",
    "gender" : "M/F",
    "self_description" : "string",
    "user_photo" : "url"
}
```

