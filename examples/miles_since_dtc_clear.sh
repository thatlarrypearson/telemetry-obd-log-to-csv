# miles_since_dtc_clear.sh
# provides a method to to get the first and last DISTANCE_SINCE_DTC_CLEAR values in an
# output file generated by distance.sh/distance.py
# 
echo file_name,first_distance,last_distance
for fname in $(ls -1 *.csv | sort)
do
    egrep -v '^,' "${fname}" | grep -v DISTANCE_SINCE_DTC_CLEAR > tmp.$$.csv
    if [ $(cat tmp.$$.csv | wc -l) -lt 2 ]
    then
        continue
    fi
    awk -F ',' '// {print $1 * 0.62137119}' < tmp.$$.csv > distance_list.txt
    echo "${fname}",$(head --lines=1 distance_list.txt),$(tail --lines=1 distance_list.txt)
    rm tmp.$$.csv distance_list.txt
done
