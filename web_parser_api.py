from bs4 import Comment
import os

# remove all comments blocks like: <!-- some comments -->
def remove_comments(soupPage):
    comments = soupPage.findAll(text=lambda text: isinstance(text, Comment))
    [it.extract() for it in comments]
    return comments

# remove all tag blocks
def remove_tags(soupPage, tags):
    [it.extract() for it in soupPage(tags)]

# return all tags by selected names
def get_tags(soupPage, tagName):
    result = []
    for it in soupPage.findAll(tagName):
        if ((not it.has_attr('style') or it.attrs["style"] != 'display: none') # is visible
            and it.string != None # is not empty
            and not it.findChildren()): # is last
            result.append(it)
    return result

# return all urls from given page
def get_all_links(soupPage):
    return get_tags(soupPage, 'a')

