#!/bin/bash

mv vuln.csv vuln_"$(date +%Y-%m-%d_%H-%M-%S)".csv
touch "vuln.csv"
mv failed.txt failed_"$(date +%Y-%m-%d_%H-%M-%S)".txt
touch "failed.txt"

for image in $(cat ./scraper-files/image-names.txt)
do
    	echo "Adding $image..."
    	success=true
		SECONDS=0
	 	while true
    	do
            	output=$(anchore-cli --url "http://localhost:8228/v1" --u "admin" --p "foobar" image add "$image:latest")
            	echo "$output" | grep "error_code=REGISTRY_PERMISSION_DENIED'}" -q && echo "Permission denied to scan image."&& echo "$image" >> failed.txt && success=false && break
				echo "$output" | grep "error_code=REGISTRY_IMAGE_NOT_FOUND'}" -q && echo "Image not found."&& echo "$image" >> failed.txt && success=false && break
				echo "$output" | grep "HTTP Code: 400" -q && echo "Unknown error occured."&& echo "$image" >> failed.txt && success=false && break
				if [ "$SECONDS" -gt "3600" ]
                then
                        echo "Timeout"&& echo "$image" >> failed.txt && success=false && break
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
