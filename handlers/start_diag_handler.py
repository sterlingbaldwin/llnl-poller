from subprocess import Popen, PIPE
from constants import USER_DATA_PREFIX
from constants import FRONTEND_POLLER_HOST
from util import print_message
from subprocess import Popen, PIPE

import requests
import json
import os
import shutil


class StartDiagHandler(object):

    def __init__(self, config):
        self.allowed_sets = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.config = config
        self.call_args = self.sanitize_input()
        # self.call_args.append('--dryrun')

    def handle(self):
        args = ' '.join(self.call_args)
        msg = "Starting job: {}".format(args)
        print_message(msg, 'ok')
        process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        output = process.communicate()
        archive_path = '{prefix}{user}/run_archives/{run_name}_{id}/'.format(
            prefix=USER_DATA_PREFIX,
            user=self.config.get('user', 'default'),
            id=self.config.get('job_id'),
            run_name=self.config.get('run_name', 'default'))
        archive_filename = archive_path + 'output_archive'

        if not os.path.exists(archive_filename + '.tar.gz'):
            try:
                print_message(
                    'creating output archive {}'.format(archive_filename + '.tar.gz'),
                    'ok')
                shutil.make_archive(
                    archive_filename,
                    'gztar',
                    self.config.get('output_dir'))
            except:
                raise
        else:
            print_message('archive {} already exists'.format(archive_filename + '.tar.gz'))
        return output

    def respond(self, response):
        msg = "Sending complete job to the dashboard with response {}".format(response)
        print_message(msg, 'ok')
        request = json.dumps({
            'job_id': self.config.get('job_id'),
            'request': 'complete',
            'output': response
        })
        url = 'http://' + FRONTEND_POLLER_HOST
        try:
            r = requests.post(url, request)
        except Exception as e:
            raise e
        return

    def sanitize_input(self):
        args = ['metadiags']
        path_prefix = "path=" + USER_DATA_PREFIX
        for x in self.config:
            print_message('key: {}\nval: {}'.format(x, self.config.get(x)))
            option_key = ''
            option_val = ''
            if x == 'diag_type':
                option_key = '--package'
                # Check for valid package
                if self.config.get(x) != 'AMWG' and self.config.get(x) != 'amwg':
                    print_message("{} is not a valid package".format(self.config.get(x)))
                    return -1
                option_val = self.config.get(x)
            elif x == 'model_path':
                option_key = "--model "
                # Check for valid paths
                if os.path.exists(self.config.get(x)):
                    option_val = 'path=' + self.config.get(x) + ',climos=yes'
                else:
                    print_message('model_path {} does not exist'.format(self.config.get(x)))
            elif x == 'obs_path':
                option_key = '--obs'
                # Check for valid obs path
                if os.path.exists(self.config.get(x)):
                    option_val = 'path=' + self.config.get(x) + ',climos=yes'
                else:
                    print_message('model_path {} does not exist'.format(self.config.get(x)))
            elif x == 'output_dir':
                option_key = '--outputdir'
                if not os.path.exists(self.config.get(x)):
                    print_message('output_dir {} does not exist'.format(self.config.get(x)))
                else:
                    option_val = self.config.get(x)
                print_message(option_val)
            elif x == 'set':
                option_key = '--set'
                sets = []
                for s in self.config.get(x):
                    if s not in self.allowed_sets:
                        print_message('invalid set: {}'.format(s))
                    else:
                        sets.append(s)
                # Check for valid set
                option_val = ' '.join(sets)
            #
            # etc etc etc moar options
            #
            else:
                print "Unrecognized option passed to diag handler: {}".format(x)
                continue
            args.append(option_key)
            args.append(option_val)
        return args
