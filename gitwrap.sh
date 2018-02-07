#!/bin/sh

echo ""
echo ""
echo ""

SCRIPT_DIR="$(cd `dirname $0` && pwd)"
ROLES_DIR="${SCRIPT_DIR}/ansible/roles"


cd $ROLES_DIR
ROLE_LIST=`find . -maxdepth 1 -type d | sed s/\\\.\\\///`

while read -r line; do
	echo -------------------------------------
	echo REPO: $line
    cd "${ROLES_DIR}/${line}"
    $*

done <<< "$ROLE_LIST"
