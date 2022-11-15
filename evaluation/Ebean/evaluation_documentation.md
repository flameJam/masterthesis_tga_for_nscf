# Target: Ebean

Ebean version (commit hash): 7152cf656b0850682bb6428ed726c98dbcf4cb4a (master branch)

Java Version: 17

File-Access-Log-Agent Version (commit hash): 62e099423e75ac60dc450cb30a481fd993ca4c6b (real_read_using_bytebuddy_1-12-12 branch)

**--> use the ./buildAgentForBranch.sh script to build the agent and put it into the right spot!**
## How to Add the Java Agent during Testing:
add the following

```XML
<build>
  	<plugins>
  		<plugin>
		    <groupId>org.apache.maven.plugins</groupId>
		    <artifactId>maven-surefire-plugin</artifactId>
		    <version>3.0.0-M4</version>
		    <configuration>
		        <argLine>-javaagent:location_of_agent</argLine>
		    </configuration>
		</plugin>
  	</plugins>
  </build>
```

to the pom.xml file.

The tests are flickering. Stopping all other programs worked relatively well to get the tests to run...

## Types I included:
**.AutoTuneServiceProvider, 
**.css, 
**.csv, 
**.DatabasePlatformProvider, 
**.DbMigration, 
**.ExtraTypeFactory, 
**.g4, 
**.GeoTypeProvider, 
**.html, 
**.interp,  
**.jpg, 
**.json, 
**.LICENSE, 
**.md, 
**.MetricFactory, 
**.mf, 
**.migrations, 
**.png, 
**.Processor, 
**.processors, 
**.properties, 
**.ScalarJsonMapper, 
**.ScalarTypeSetFactory, 
**.ServerCachePlugin, 
**.SpiContainerFactory, 
**.SpiDdlGeneratorProvider, 
**.SpiFetchGroupService, 
**.SpiJsonService, 
**.SpiLoggerFactory, 
**.SpiProfileLocationFactory, 
**.SpiRawSqlService, 
**.sql, 
**.tokens, 
**.txt, 
**.XmapService, 
**.xml, 
**.xsd, 
**.yaml, 
**.yml, 


## Used Results:

**all tests passed in real_read and no_real_read**


coverage reports:
coverage_reports/**

assessments:
assessments/**

## How to Execute the tests

use the `execute_(no_)real_read_tests_with_agent.sh`

## Changes in source-code files:
I considered all *.java files source-code