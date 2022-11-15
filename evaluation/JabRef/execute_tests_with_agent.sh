#!/bin/bash

export FILE_ACCESS_AGENT_REPOSITORY=<LOCATION_OF_JABREF>
export FILE_ACCESS_AGENT_DEBUG=false

OUTPUT_DIR=<OUTPUT_DIR>

TEST_DATE=$(date +"%Y-%m-%d_%H-%M-%S")

export FILE_ACCESS_AGENT_REAL_READ=false
export FILE_ACCESS_AGENT_OUTPUT=$OUTPUT_DIR/jabref_coverage_report_

echo "Executing tests with FileAccessAgent, without real_read"
./gradlew clean test --rerun-tasks
echo "Done"

exit

echo "Copying report"
cp -r build/reports/test $OUTPUT_DIR/../${TEST_DATE}_test_report
echo "Copying Done"

export FILE_ACCESS_AGENT_REAL_READ=true
export FILE_ACCESS_AGENT_OUTPUT=$OUTPUT_DIR/real_read_jabref_coverage_report_

echo "Executing tests with FileAccessAgent, with real_read"
./gradlew clean test --rerun-tasks
echo "Done"

echo "Copying report"
cp -r build/reports/test $OUTPUT_DIR/../${TEST_DATE}_real_read_test_report
echo "Copying Done"

exit