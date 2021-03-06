#
# A list of constants for the job poller
#

# hostname of the server running the frontend poller application
FRONTEND_POLLER_HOST = 'aims2.llnl.gov:8000/poller/update/'

# hostname of the diagnostic output viewer
DIAG_VIEWER_HOST = 'http://pcmdi10.llnl.gov:8008/'

# diagnostic path base
DIAG_PATH_PREFIX = '/export/baldwin32/diags'

# hardcoded directory prefix for where to move the output to
# Im hard coding this instead of doing relative paths
# because the poller and the dashboard should live on
# differenct servers with a jointly mounted drive
# but the configuration hasnt been hammered out yet
USER_DATA_PREFIX = '/export/baldwin32/projects/acme-web-fe/userdata/'
