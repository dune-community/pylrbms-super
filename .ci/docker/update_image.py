#!/usr/bin/env python3

import os
import subprocess
import sys
import bottle
import threading
import six
import re
try:
    import docker
except ImportError:
    print('missing module: pip install docker')
    sys.exit(1)
from docker.utils.json_stream import json_stream

cc_mapping = {'gcc': 'g++', 'clang': 'clang++'}
thisdir = os.path.dirname(os.path.abspath(__file__))

URL = 'http://localhost:17777'


@bottle.route('/token')
def token():
    return os.environ['ZIVGITLAB_TOKEN']


def _build(client, **kwargs):
    resp = client.api.build(**kwargs)
    if isinstance(resp, six.string_types):
        return client.images.get(resp), []
    last_event = None
    image_id = None
    output = []
    for chunk in json_stream(resp):
        if 'error' in chunk:
            msg = chunk['error'] + '\n' + ''.join(output)
            raise docker.errors.BuildError(msg, chunk)
        if 'stream' in chunk:
            output.append(chunk['stream'])
            match = re.search(
                r'(^Successfully built |sha256:)([0-9a-f]+)$',
                chunk['stream']
            )
            if match:
                image_id = match.group(2)
        last_event = chunk
    if image_id:
        return client.images.get(image_id), output
    raise docker.errors.BuildError(last_event or 'Unknown', '\n'.join(output))


def update(commit, refname, cc):
    pylrbms_super_dir = os.path.join(thisdir, '..', '..',)
    dockerfile = os.path.join(thisdir, 'pylrbms-testing', 'Dockerfile')
    client = docker.from_env(version='auto')

    os.chdir(pylrbms_super_dir)

    cxx = cc_mapping[cc]
    repo = 'dunecommunity/pylrbms-testing_{}'.format(cc)

    buildargs = {'cc': cc, 'cxx': cxx, 'commit': commit,
                'URL': URL}
    tag = '{}:{}'.format(repo, commit)
    img,out = _build(client, rm=True, fileobj=open(dockerfile, 'rb'), pull=True,
                tag=tag, buildargs=buildargs, nocache=False, network_mode='host')
    img.tag(repo, refname)
    img.tag(repo, commit)
    client.images.push(repo, tag=refname)
    client.images.push(repo, tag=commit)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        ccs = [sys.argv[1]]
    else:
        ccs = list(cc_mapping.keys())

    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], universal_newlines=True).strip()
    commit = os.environ.get('CI_COMMIT_SHA', head)
    refname = os.environ.get('CI_COMMIT_REF_NAME', 'master').replace('/', '_')

    webserver = threading.Thread(target=bottle.run, kwargs=dict(host='localhost', port=17777))
    webserver.daemon = True
    webserver.start()
    subprocess.check_call(['docker', 'pull', 'dunecommunity/testing-base_debian:latest'])
    for c in ccs:
        try:
            update(commit, refname, c)
        except docker.errors.BuildError as be:
            print(be.msg)
            break
    webserver.join(1)
