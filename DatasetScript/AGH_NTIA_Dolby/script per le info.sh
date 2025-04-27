#!/bin/bash

DIRECTORY="/home/greco/home/datasets/IGVQM/AGH_NTIA_Dolby/y4m/pvs"
OUTPUT_FILE="/home/greco/home/docker/distorted_updated.json"

echo "[" > "$OUTPUT_FILE"

id=1

for file in "$DIRECTORY"/*; do
    if [[ -f "$file" && "$file" != *_original* ]]; then

        file_name=$(basename "$file")
        duration=$(mediainfo --Inform="General;%Duration/String3%" "$file" | cut -d':' -f3)
        bitrate=$(mediainfo --Inform="General;%OverallBitRate/String%" "$file" | sed 's/[^0-9]*//g')
        fps=$(mediainfo --Inform="General;%FrameRate/String%" "$file" | cut -d' ' -f1)

        width=$(mediainfo --Inform="Video;%Width%" "$file")
        height=$(mediainfo --Inform="Video;%Height%" "$file")
        
        video_codec="YUV"  
        pixel_format=$(mediainfo --Inform="Video;%ChromaSubsampling%" "$file")
        if [[ "$pixel_format" == "4:2:0" ]]; then
            pixel_format="420"
        elif [[ "$pixel_format" == "4:2:2" ]]; then
            pixel_format="422"
        fi
        
        bitdepth="8"

        json_line=$(jq -n \
            --arg id "$id" \
            --arg file_name "$file_name" \
            --arg width "$width" \
            --arg height "$height" \
            --arg bitrate "$bitrate" \
            --arg video_codec "$video_codec" \
            --arg bitdepth "$bitdepth" \
            --arg pixel_format "$pixel_format" \
            --arg fps "$fps" \
            --arg duration "$duration" \
            '{
                id: ($id | tonumber),
                file_name: $file_name,
                width: ($width | tonumber),
                height: ($height | tonumber),
                bitrate: ($bitrate | tonumber),
                video_codec: $video_codec,
                bitdepth: ($bitdepth | tonumber),
                pixel_format: $pixel_format,
                fps: ($fps | tonumber),
                duration: ($duration | tonumber)
            }')

        echo "$json_line," >> "$OUTPUT_FILE"
        
        id=$((id + 1))
    fi
done

if [[ $id -eq 1 ]]; then
    echo "No file found." 
    echo "[]" > "$OUTPUT_FILE" 
else
    sed -i '$ s/,$//' "$OUTPUT_FILE"
    echo "]" >> "$OUTPUT_FILE"
fi
