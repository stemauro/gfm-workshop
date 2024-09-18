#!/usr/bin/env bash

if [ -z "$curr_dir" ]; then
    curr_file="${BASH_SOURCE[0]:-${(%):-%x}}"
    curr_dir="$(dirname "$curr_file")"
fi

venv_dir="$curr_dir"/env-"$SYSTEMNAME"

[ -x "$(command -v deactivate)" ] && deactivate

module --force purge
if ! [ -f "$curr_dir"/modules.sh ]; then
    echo "Cannot find \`$curr_dir/modules.sh\`; its existence is required."
    exit 1
fi
source "$curr_dir"/modules.sh

if ! [ -d "$venv_dir" ]; then
    echo "Please manually execute \`nice bash ${curr_dir@Q}/setup.sh\`" \
         "on a login node to create the \`venv\`."
    exit 1
elif ! [ -f "$venv_dir"/bin/activate ]; then
    echo "Something seems to be wrong with the \`venv\` at \`$venv_dir\`." \
         "Please delete it (\`nice rm -rf ${venv_dir@Q}\`) and" \
         "execute \`nice bash ${curr_dir@Q}/setup.sh\`" \
         "on a login node to re-create the \`venv\`."
    exit 1
fi
source "$venv_dir"/bin/activate
