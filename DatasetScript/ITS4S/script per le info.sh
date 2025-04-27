#!/bin/bash

DIRECTORY="/home/greco/home/datasets/IGVQM/ITS4S/compressed"
OUTPUT_FILE="/home/greco/home/docker/ITS4S.json"

echo "[" > "$OUTPUT_FILE"

id=1

for file in "$DIRECTORY"/*; do
    if [[ -f "$file" ]]; then
        file_name=$(basename "$file")
        width=$(mediainfo --Inform="Video;%Width%" "$file")
        height=$(mediainfo --Inform="Video;%Height%" "$file")
        bitrate=$(mediainfo --Inform="Video;%BitRate/String%" "$file" | sed 's/[^0-9]*//g')
        
        format=$(mediainfo --Inform="Video;%Format%" "$file")
        video_codec=""
        if [[ "$format" == "AVC" ]]; then
            video_codec="x264"
        else
            video_codec=$(mediainfo --Inform="Video;%Codec%" "$file")
        fi
        
        bitdepth=$(mediainfo --Inform="Video;%BitDepth%" "$file")
        
        pixel_format=$(mediainfo --Inform="Video;%ChromaSubsampling%" "$file")
        if [[ "$pixel_format" == "4:2:0" ]]; then
            pixel_format="420"
        fi
        
        fps=$(mediainfo --Inform="Video;%FrameRate%" "$file" | cut -d' ' -f1)
        duration=$(mediainfo --Inform="General;%Duration/String3%" "$file" | cut -d':' -f3)

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

sed -i '$ s/,$//' "$OUTPUT_FILE"
echo "]" >> "$OUTPUT_FILE"
