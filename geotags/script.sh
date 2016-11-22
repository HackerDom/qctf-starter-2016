#!/bin/bash
input="points.csv"

images=(images/*.jpg)
filenumber=0

while IFS=';' read -r lat long other
do
    exiftool -GPSLongitudeRef=E -GPSLongitude=$long -GPSLatitudeRef=N -GPSLatitude=$lat -overwrite_original ${images[$filenumber]}
    echo "Image number $filenumber was updated"
    ((filenumber++))
done < "$input"

