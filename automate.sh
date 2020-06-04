#!/bin/bash

#Automate the process of analyzing Docker images using the Anchore Engine vulnerability scanner
#Copyright (C) 2020 Katrine Wist and Malene Helsem

#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

mv vuln.csv vuln_"$(date +%Y-%m-%d_%H-%M-%S)".csv
touch "vuln.csv"
mv failed.txt failed_"$(date +%Y-%m-%d_%H-%M-%S)".txt
touch "failed.txt"

for image in $(cat ./image-names.txt)
do
    echo "Adding $image..."
    success=true
    SECONDS=0
    while true
    do
        output=$(anchore-cli --url "http://localhost:8228/v1" --u "admin" --p "foobar" image add "$image:latest")
        echo "$output" | grep "error_code=REGISTRY_PERMISSION_DENIED'}" -q && echo "Permission denied to scan image." && echo "$image,permission_denied" >> failed.txt && success=false && break
        echo "$output" | grep "error_code=REGISTRY_IMAGE_NOT_FOUND'}" -q && echo "Image not found."&& echo "$image,not_found" >> failed.txt && success=false && break
        echo "$output" | grep "HTTP Code: 400" -q && echo "Unknown error occured." && echo "$image,unknown_error" >> failed.txt && success=false && break
        if [ "$SECONDS" -gt "3600" ]
        then
            echo "Timeout"&& echo "$image,timeout" >> failed.txt && success=false && break
	    fi
	    echo "$output" | grep "Analysis Status: analyzed" -q && break || (echo "Not finished, sleeping..." && sleep 20)
    done
    if $success
    then
        echo "Finished, writing result to file..."
        if [[ $(anchore-cli --url "http://localhost:8228/v1" --u "admin" --p "foobar" image vuln "$image:latest" all) ]]
        then
            anchore-cli --url "http://localhost:8228/v1" --u "admin" --p "foobar" image vuln "$image:latest" all | sed -r 's/,/;/g' |sed -r 's/  +/,/g'| sed 's/,$//' | egrep -v '^Vulnerability ID' | awk '{ print "'"$image"',"$1 }' | awk -F, -v OFS=, '{ if(NF==6) { k=$NF; $6=""; $7=k; print } else { for ( i=NF; i<=7; i++ ) { $i=$i"" } print }}' >> vuln.csv
    	else
            echo "No found vulnerabilities"
    	fi

    fi
done
