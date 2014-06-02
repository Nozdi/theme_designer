"""
.. module:: gcs
    :synopsis: Module for connecting with google cloud storage
"""

import cloudstorage as gcs
import os
from google.appengine.api import app_identity

DEBUG = True

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)

gcs.set_default_retry_params(my_default_retry_params)

BUCKET_NAME = os.environ.get('BUCKET_NAME',
                             app_identity.get_default_gcs_bucket_name())


def create_file(filename, data):
    """
    Create a file.
    """
    path = "/{}/{}".format(BUCKET_NAME, filename)

    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(path,
                        'w',
                        options={'x-goog-acl':'public-read'},
                        content_type='application/octet-stream',
                        retry_params=write_retry_params)
    gcs_file.write(data)
    gcs_file.close()
    if DEBUG:
        return "http://localhost:8080/_ah/gcs" + path
    return "https://storage.googleapis.com" + path


def delete_file(link):
    try:
        gcs.delete("/{}/{}".format(BUCKET_NAME, "/".join(link.split("/")[-2:])))
    except gcs.NotFoundError:
        pass
