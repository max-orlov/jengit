########
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
############
import argh

import yaml
from path import path


class Configuration(object):

    def save(self,
             repo_root_dir,
             reset=False):
        if not self.conf_dir.exists():
            self.conf_dir.mkdir()
        conf = self.conf_dir / 'config.yaml'
        if conf.exists() and not reset:
            raise argh.CommandError('Already initialized. '
                                    'Run "jit init --reset"')

        conf.write_text(yaml.safe_dump({
            'repo_root_dir': repo_root_dir,
        }, default_flow_style=False))

    @property
    def conf_dir(self):
        return path('~/.jengit').expanduser()

    @property
    def conf(self):
        conf = self.conf_dir / 'config.yaml'
        if not conf.exists():
            raise argh.CommandError('Not initialized. Run "jit init"')
        return yaml.safe_load(conf.text())

    @property
    def root_repos_dir(self):
        return self.conf.get('repo_root_dir')


configuration = Configuration()
