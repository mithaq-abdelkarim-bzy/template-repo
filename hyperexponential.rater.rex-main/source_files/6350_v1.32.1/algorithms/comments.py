import hx
from datetime import date

def add_new_comment(hxd):
    '''
    Async task that adds comments to the comment table
    '''

    hxd.comments.show_comment_input_box = False
    hxd.comments.hide_comment_input_box = True
    hxd.comments.comments_table = hxd.temp.comments.comments_table

    if hxd.comments.comment_input_box:
        hxd.comments.comments_table.insert(0, 
            {
            "comment": hxd.comments.comment_input_box, 
            "created_date": date.today().strftime('%Y-%m-%d'),
            "created_by": hx.meta.user.name
            }
        )


def start_add_comments(hxd):
    '''
    Async task that stores the comment table into temp storage
    and enable user to enter comments
    '''

    hxd.comments.show_comment_input_box = True
    hxd.comments.hide_comment_input_box = False
    hxd.temp.comments.comments_table = hxd.comments.comments_table


    