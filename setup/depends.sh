#!/bin/bash

#    Copyright 2012
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

if [ "$(id -u)" != "0" ]; then
    echo "[!] This script must be run as root." 1>&2
    exit 1
fi

echo "[*] Installing packages ..."
apt-get install python-pip python-dev build-essential mysql-server memcached libmemcached-dev python-mysqldb python-mysqldb-dbg zlib1g-dev

echo "[*] Installing python libs ..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
sh "$DIR/python-depends.sh"

echo ""
echo "[*] Setup Completed."
