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

    params = dict(movieId=query, attributes='1', mediaType='streaming')
    url = 'http://www.canistream.it/services/query'

    r = web.get(url, params)

    r.raise_for_status()

    results = r.json()

    if len(results) > 0:
        for key, value in results.iteritems():
            wf.add_item(title=value['friendlyName'],
                        subtitle=str('View on ' + value['friendlyName']),
                        uid=value['external_id'],
                        arg=value['direct_url'],
                        valid=True,
                        icon='images/' + key + '.png')
    else:
        wf.add_item('No streaming options available.')
    #
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
