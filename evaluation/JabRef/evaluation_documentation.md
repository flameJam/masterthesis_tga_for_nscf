# Evaluation 1, beginning on 03.10.2022
Target: [Jabref](https://github.com/JabRef/jabref)

Jabref version (commit hash): 1797af8e3bcc6105563b337223e5257abc97ca35 (main branch)

Java Version: 17 (has to be changed in build.gradle)

File-Access-Log-Agent Version (commit hash): def8f54c63b1c8297b27e3dc0ff1c52d344b8306 (real_read_dev branch)

**--> use the ./buildAgentForBranch.sh script to build the agent and put it into the right spot!**
## How to Add the Java Agent during Testing:
add

`test.jvmArgs '-javaagent:location_of_agent'`

to the test task in gradle.build

## How to Execute the tests

removed the remove the "excludeTags" thingy from the test task

also add maxParallelForks=6 to the gradle.build file in the test task, otherwise the real_read_version will have Java Heap Space Out-of-memory problems

execute the script "execute_tests_with_agent.sh" from the repository's root directory

## Test results

coverage_reports/**
assessments/**


## Interesting File types:
I excluded:
- **.java
- **.class

interesting:
- **.bat, 
- **.bib, 
- **.bmp, 
- **.bpmn, 
- **.bst, 
- **.cff, 
- **.CNAME, 
- **.connect-plug-etc-chromium-native-messaging-jabref, 
- **.connect-plug-etc-opt-chrome-native-messaging-jabref, 
- **.connect-plug-etc-opt-edge-native-messaging-jabref, 
- **.connect-plug-hostfs-mozilla-native-messaging-jabref, 
- **.copyright, 
- **.csl, 
- **.css, 
- **.ctv6bak, 
- **.desktop, 
- **.disconnect-plug-etc-chromium-native-messaging-jabref, 
- **.disconnect-plug-etc-opt-chrome-native-messaging-jabref, 
- **.disconnect-plug-etc-opt-edge-native-messaging-jabref, 
- **.disconnect-plug-hostfs-mozilla-native-messaging-jabref, 
- **.docx, 
- **.entitlements, 
- **.enw, 
- **.epf, 
- **.fxml, 
- **.g4, 
- **.Gemfile, 
- **.gif, 
- **.gitignore, 
- **.gradle, 
- **.gradlew, 
- **.groovy, 
- **.icns, 
- **.ico, 
- **.IkonHandler, 
- **.IkonProvider, 
- **.isi, 
- **.JabRef-launcher, 
- **.jar, 
- **.jks, 
- **.json, 
- **.jstyle, 
- **.layout, 
- **.lock, 
- **.MAINTAINERS, 
- **.md, 
- **.mimetype, 
- **.MockMaker, 
- **.mv, 
- **.nbib, 
- **.no_enw, 
- **.pdf, 
- **.plist, 
- **.png, 
- **.postinst, 
- **.postinstall, 
- **.postrm, 
- **.PresenterFactory, 
- **.properties, 
- **.ps1, 
- **.py, 
- **.Rakefile, 
- **.rb, 
- **.readme, 
- **.README, 
- **.ResourceLocator, 
- **.ris, 
- **.scpt, 
- **.sh, 
- **.spec, 
- **.sql, 
- **.svg, 
- **.template, 
- **.terms, 
- **.test, 
- **.tex, 
- **.tiff, 
- **.ttf, 
- **.txt, 
- **.uml, 
- **.Writer, 
- **.wsf, 
- **.xjb, 
- **.xml, 
- **.xsd, 
- **.xsl, 
- **.yaml, 
- **.yml,



## irrelevant directories
exclude due to size: /buildres/csl/csl-styles/dependent (has 7830 entries)

- docs
- licenses

## Changes in source-code files:
I considered all *.java files source-code