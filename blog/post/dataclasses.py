from pydantic import BaseModel, constr, validator


class PostAuthor(BaseModel):

    username: constr(max_length=50) | None
    user_image: str | None
    user_info: str | None


class Filters(BaseModel):
    """
    Conversion filters for sorting a post in blog, in JSON in to comfort python dict, with validation.

    In the fields with the prefix "post" at the beginning, we pass the conditions
    for filtering that match the word after the underscore

    in the field "sort mode" you can pass only such values:
            'recommended' - if you want to sort posts from most popular to least (based on likes)
            'new' - if you want to sort posts by release date, newest first
    """
    post_title: constr(max_length=100) | None
    post_rubric: str | None
    post_tags: list[str] | None
    sorting_mode: str | None
    post_author: str | None

    @validator('sorting_mode')
    def is_correct_sorting_mode(cls, sorting_mode):
        correct_sorting_mode = ['recommended', 'nuw']

        if sorting_mode in correct_sorting_mode:
            return sorting_mode
        else:
            raise ValueError(f"{sorting_mode} wrong sorting_mode. List of possible mode - ['recommended', 'nuw']")
