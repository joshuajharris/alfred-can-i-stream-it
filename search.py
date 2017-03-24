#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow, ICON_WEB, ICON_INFO, web

__version__ = 'v1.0.0'

GITHUB_SLUG = 'joshuajharris/alfred-can-i-stream-it'
UPDATE_SETTINGS = {
    'github_slug': GITHUB_SLUG,
    'version': __version__
}

SERVICES_URL = 'http://www.canistream.it/services'

def getJSON(url, params):
    r = web.get(url, params)
    r.raise_for_status()
    return r.json()

def search(query):
    url = SERVICES_URL + '/search'
    params = dict(movieName=query)

    return getJSON(url, params)

def stream(movieId):
    url = SERVICES_URL + '/query'
    params = dict(movieId=movieId, attributes='1', mediaType='streaming')

def main(wf):
    # If query is set strip white space at ends
    # If not, set to "None"
    query =  wf.args[0].strip() if len(wf.args) else None

    if query is not None:
        results = search(query)

    if len(results) > 0:
        for movie in results:
            wf.add_item(title=movie['title'],
                        subtitle=str(movie['year']),
                        uid=movie['_id'],
                        arg=movie['_id'],
                        valid=True,
                        icon=ICON_WEB)
                        # icon=movie['image'])
    else:
        wf.add_item('No movies by that name found.')

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but Alfred won't be listening
    # any more...
    wf.send_feedback()

if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow(update_settings=UPDATE_SETTINGS)
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item('New version available',
                    'Action this item to install the update',
                    autocomplete='workflow:update',
                    icon=ICON_INFO)

    sys.exit(wf.run(main))
