#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow, ICON_WEB, web


def main(wf):

    if wf.update_available:
        wf.add_item("An update is available!",
                    autocomplete='workflow:update', valid=False)
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`. Not so useful, as
    # the `wf` object created in `if __name__ ...` below is global.
    #
    # Your imports go here if you want to catch import errors (not a bad idea)
    # or if the modules/packages are in a directory added via `Workflow(libraries=...)`

    # Get args from Workflow, already in normalized Unicode
    # Get query from Alfred
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    # params = dict(movieId='4eb04794f5f8077d1d000000', attributes='1', mediaType='streaming')
    # url = 'http://www.canistream.it/services/query'
    params = dict(movieName=query)
    url = 'http://www.canistream.it/services/search'

    r = web.get(url, params)

    r.raise_for_status()

    results = r.json()

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
    wf = Workflow()
                #   update_settings={
                #       'github_slug': '',
                #       'version': 'v1.0.0'
                #   })
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))
