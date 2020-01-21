#!/bin/sh

mv vuln.csv vuln_"$(date +%Y-%m-%d_%H-%M-%S)".csv

for image in $(cat testImageNames.txt)
do
    	echo "Adding $image..."
    	success=true
    	while true
    	do
            	output=$(anchore-cli --url "http://localhost:8228/v1" --u "admin" --p "foobar" image add "$image:latest")
            	echo "$output" | grep "error_code=REGISTRY_PERMISSION_DENIED'}" -q && echo "Permission denied to scan image." && success=false && break
            	echo "$output" | grep "Analysis Status: analyzed" -q && break || (echo "Not finished, sleeping..." && sleep 10)
    	done
    	if $success
    	then
            	echo "Finished, writing result to file..."
            	anchore-cli --url "http://localhost:8228/v1" --u "admin" --p "foobar" image vuln "$image:latest" all | sed -r 's/  +/,/g' | sed 's/,$//' | egrep -v '^Vulnerability ID' | awk '{ print "'"$image"',"$1 }' >> vuln.csv
    	fi
done

