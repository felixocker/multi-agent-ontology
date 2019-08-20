@echo off
REM place this batch file into your stardog\bin directory and run there
REM adapt variable path-to-dir as necessary
set "path-to-dir=C:\Users\Ocker\LRZ Sync+Share\ProductAgentOntology\implementation\"
start stardog-admin.bat server start
@echo on
timeout 5
call stardog-admin.bat db drop PAonto & ^
call stardog-admin.bat db create -n PAonto "%path-to-dir%PAonto.ttl" && ^
call stardog.bat query PAonto "%path-to-dir%queryingPAonto\featConsistency.sparql" &&  ^
call stardog.bat query PAonto -f CSV "%path-to-dir%queryingPAonto\pa-states.sparql" > "%path-to-dir%queryingPAonto\pa-states.csv" &&  ^
echo "created pa-states.csv" &&  ^
call stardog.bat query PAonto -f CSV "%path-to-dir%queryingPAonto\pa-transitions.sparql" > "%path-to-dir%queryingPAonto\pa-transitions.csv"  &&  ^
echo "created pa-transitions.csv" &&  ^
call stardog.bat query PAonto -f CSV "%path-to-dir%queryingPAonto\ra-freeCapa.sparql" > "%path-to-dir%queryingPAonto\ra-freeCapa.csv" &&  ^
echo "created ra-freeCapa.csv" &&  ^
call stardog.bat query PAonto -f CSV "%path-to-dir%queryingPAonto\ra-feats.sparql" > "%path-to-dir%queryingPAonto\ra-feats.csv" &&  ^
echo "created ra-feats.csv" &&  ^
call stardog-admin.bat server stop