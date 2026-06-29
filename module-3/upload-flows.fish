#!/usr/bin/env fish

set script_dir (cd (dirname (status --current-filename)); and pwd)
set flows_dir "$script_dir/flows"
set upload_url "http://localhost:28080/api/v1/flows/import"
set credentials "admin@kestra.io:Admin1234!"

if not test -d "$flows_dir"
    echo "Flows directory not found: $flows_dir" >&2
    exit 1
end

set flow_files "$flows_dir"/*.yaml

if not test -e $flow_files[1]
    echo "No YAML flow files found in $flows_dir" >&2
    exit 1
end

for flow_file in $flow_files
    echo "Uploading "(basename "$flow_file")"..."
    curl -X POST \
        -u "$credentials" \
        "$upload_url" \
        -F "fileUpload=@$flow_file"
    or exit 1
end
