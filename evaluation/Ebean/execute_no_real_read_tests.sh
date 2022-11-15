#!/bin/bash

export FILE_ACCESS_AGENT_REPOSITORY=<LOCATION_OF_EBEAN>
export FILE_ACCESS_AGENT_DEBUG=false

OUTPUT_DIR=<OUTPUT_DIR>

TEST_DATE=$(date +"%Y-%m-%d_%H-%M-%S")

JAVA_AGENT=<LOCATION_OF_AGENT_JAR>

export FILE_ACCESS_AGENT_REAL_READ=false
export FILE_ACCESS_AGENT_OUTPUT=$OUTPUT_DIR/ebean_coverage_report_

echo "Executing tests with FileAccessAgent, with real_read"
mvn clean test
echo "Done"

exit


