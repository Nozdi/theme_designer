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

if not BUCKET_NAME:
    BUCKET_NAME = 'app_default_bucket'


def create_file(filename, data):
    """
    Create a file.
    """
    path = "/{}/{}".format(BUCKET_NAME, filename)

    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(path,
                        'w',
                        content_type='application/octet-stream',
                        # options={'x-goog-project-id': 405390963802},
                        # options={'x-goog-meta-foo': 'foo',
                        #          'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    gcs_file.write(data)
    gcs_file.close()
    if DEBUG:
        return "http://localhost:8080/_ah/gcs" + path
    return "theme-designer.storage.googleapis.com{}".format(path)
