#!/usr/bin/env bash
#
# IMPORTANT: Change this file only in directory Standalone!

if [${PORT}]; then
    java ${JAVA_OPTS} -jar /opt/selenium/selenium-server-standalone.jar \
        ${SE_OPTS} -port ${PORT}
else
    java ${JAVA_OPTS} -jar /opt/selenium/selenium-server-standalone.jar \
        ${SE_OPTS}
fi