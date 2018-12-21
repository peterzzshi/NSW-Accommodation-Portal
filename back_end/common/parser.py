import re,sys

def token_parser(token):
    userID = int(re.search(r"id(\d+)_",token).group(1))
    timepoint = float(re.sub(r'.*_','',token))
    return userID, timepoint
