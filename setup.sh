#!/usr/bin/env bash

curr_file="${BASH_SOURCE[0]:-${(%):-%x}}"
curr_dir="$(dirname "$curr_file")"

venv_dir="$curr_dir"/env-"$SYSTEMNAME"

if ! [ -d "$venv_dir" ]; then
    [ -x "$(command -v deactivate)" ] && deactivate

    module --force purge
    if ! [ -f "$curr_dir"/modules.sh ]; then
        echo "Cannot find \`$curr_dir/modules.sh\`; its existence is required."
        exit 1
    fi
    source "$curr_dir"/modules.sh

    python3 -m venv --system-site-packages "$venv_dir"

    if ! [ -f "$venv_dir"/bin/activate ]; then
        echo "Something seems to be wrong with the \`venv\` at \`$venv_dir\`." \
             "Please delete it (\`nice rm -rf ${venv_dir@Q}\`) and" \
             "execute \`nice bash ${curr_dir@Q}/setup.sh\`" \
             "on a login node to re-create the \`venv\`."
        exit 1
    fi
    source "$venv_dir"/bin/activate

    python -m pip install -U pip
    if ! [ -f "$curr_dir"/requirements.txt ]; then
        echo "Cannot find \`$curr_dir/requirements.txt\`;" \
             "its existence is required."
        exit 1
    fi
    python -m pip install --no-cache-dir -r "$curr_dir"/requirements.txt

    deactivate
else
    echo "\`venv\` is already set up at \`$venv_dir\`. Please" \
         "delete it (\`nice rm -rf ${venv_dir@Q}\`) to force a re-generation."
fi
