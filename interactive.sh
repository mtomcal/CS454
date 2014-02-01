#!/bin/bash

echo 'Mkdir tmp...'
mkdir -p /tmp/mtomcal
if ( [ "${1}" != "" ] ) ; then
echo 'Copying to tmp...'
cp -rf ${1} /tmp/mtomcal/
fi
echo 'Launching Screen...'
screen
echo -n 'Copy back to home? [y/n]: '
read mv 
if ( [ "$mv" == "y" ] ) ; then
echo 'Copying to home...'
cp -rf /tmp/mtomcal/* ~/
fi
echo -n 'Delete? [y/n]: '
read del
if ( [ "$del" == "y" ] ) ; then
echo 'Deleting...'
rm -rf /tmp/mtomcal
fi
exit
