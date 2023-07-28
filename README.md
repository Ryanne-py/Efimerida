# Efimerida
This RESTful API is for a site running blogging systems.
# Description
For posts there is a system of topics and tags, reactions (likes, comments) and the ability to subscribe to the author.
# Start instructions

Clone the repository 

    git clone https://github.com/Ryanne-py/Efimerida.git

Creating a venv

    python -m venv venv

Activate in a venv:

windows

    venv\Scripts\activate
another os

    source venv/bin/activate
Install packages

    pip install -r requirements.txt
Start (In the project folder "Efimerida\blog)
    

    python manage.py runserver
# Documentation

After installing and running the local server, the API URL will be `http://127.0.0.1:8000/`

We will analyze the ways for communication with accounts and users. The account system works on the principle of tokens, the token is placed in the http request header, in the form- `
Authorization: Token <user_token>`.
Thus, requests to the API will be made on behalf of the user whose token will be written in the headers.

## Account registration

`method POST`

    http://127.0.0.1:8000/user/registration/    

post request body

```
{
    "username": "<username>",
    "password": "<password>",
    "email": "<email>"
}
```

The user's token is stored in the response

## Account authentication

`method POST`

    http://127.0.0.1:8000/user/authentication/    

post request body

```
{
    "email": "<email>",
    "password": "<password>"
}
```

The user's token is stored in the response

## List of account

`method GET`

    http://127.0.0.1:8000/user/list/

## Account detail

`method GET PUT DELETE`

    http://127.0.0.1:8000/user/detail/
    
    
Interaction with posts

## Post list

With the GET method we get an unsorted list of all posts, with the POST method we create a new post

`method GET POST`

    http://127.0.0.1:8000/post/list/


## Post detail

Using the GET method we get all the information about the post, using the PUT method we change a specific post, with method DELETE, request deleted post

`method GET PUT DELETE`

    http://127.0.0.1:8000/post/detail/<post_id>/


## Post like

With the POST method, a like is placed on a post. When DELETING, the like is removed from the post

`method POST DELETE`

    http://127.0.0.1:8000/post/like/<post_id>/
    
## Post by filter

With the POST method, a like is placed on a post. When DELETING, the like is removed from the post

`method POST`

    http://127.0.0.1:8000/post/by_filter/
    
post request body

```
{
    "post_author:": "<username>",
    "post_title:": <title_text>",
    "post_rubric": "<post_rubric>",
    "post_tags": ["tags1", "tag2", "tag3"],
    "sorting_mode": "<sorting_mode>",
}
```
Filters can be transferred selectively, not all at once
In all filters with the prefix post (`post_title, post_rubric, post_tags`), ust insert the value to filter the post

in the field `"sorting_mode"` you can pass only such values:

   `'recommended'` - if you want to sort posts from most popular to least (based on likes)
           
   `'new'` - if you want to sort posts by release date, newest first
   
Here are a couple of examples that will help to better describe the principle of operation.

Request body that selects the newest posts whose title contains "Gameplay gta 6"

```
{
    "post_title:": "Gameplay gta 6",
    "sorting_mode": "new",
}
```

Request body that selects the most popular programming posts tagged "java-script", "react", "lesson".

```
{
    "post_rubric": "programing",
    "post_tags": ["java-script", "react", "lesson"],
    "sorting_mode": "recomended",
}
```

Request body that fetches popular posts about philosophy
```
{
    "post_tag": ["phelosofy"],
    "sorting_mode": "recomended"
}
```

## Comment list

A request with the GET method will return a list of comments under a specific post (whose id is specified in the url), with the POST method the request will create a new comment under the selected post

`method GET POST`

    http://127.0.0.1:8000/post/comment/<post_id>/
    
## Comment detail

A request with a GET method returns a specific comment under the id specified in the URL, a PUT request modifies that comment, DELETE therefore deletes

`method GET PUT DELETE`

    http://127.0.0.1:8000/post/comment_detail/<comment_id>/
    
## Rubric list

The logic is identical, it only takes into account that only users with administrator status can create rubrics

`method GET POST`

    http://127.0.0.1:8000/post/rubric_list/
    
## Rubric detail

Only admins can delete or edit a category

`method GET PUT DELETE`

    http://127.0.0.1:8000/post/rubric_detail/<rubric_id>/

## Tag detail
Use the PUT method to change a tag, the GET method to see its details, and the DELETE method to delete it

`method GET PUT DELETE`

    http://127.0.0.1:8000/post/tag_detail/<tag_id>/

## Tag list
At GET you can see the list of tags, and their data, the number of times the tag has been used in posts. In POST you can create a new tag

`method GET POST`

    http://127.0.0.1:8000/post/tag_list/

## Subscribe

`method POST DELETE`

    http://127.0.0.1:8000/user/subscribe/<int:user_id>/

## Get subscriptions

Getting a list of authors to which the user is subscribed

`method GET`
 
    http://127.0.0.1:8000/user/get_subscribe/

## Posts of users to which the user is subscribed
Posts of users that the user is following, starting with new ones

`method GET`
 
    http://127.0.0.1:8000/user/by_sub/

## Adding a post to a draft
Adding a post to a draft. Only the owner of the post can add a post to a draft
or remove it from there. After adding a post to a draft, it becomes unavailable for viewing and does not appear in feeds

`method POST DELETE`
 
    http://127.0.0.1:8000/user/draft/<int:post_id>/

## Adding a post to bookmark
Adding a post to bookmarks. Only registered user can do this. By POST method and passing the post id you can add the post to your bookmarks, by GET method you can get your list of bookmarks, by DELETE method you can delete the post from your bookmarks.

To see the list, put any numeric value in the post id field, e.g. 0

`method GET POST DELETE`
 
    http://127.0.0.1:8000/user/bookmarks/<int:post_id>/

