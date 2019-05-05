#!/usr/bin/env bash

cd ./dist/firefox/

for file in */  ; do
  if [[ -d "$file" && ! -L "$file" ]]; then
    echo "Processing ... $file";
    cd ${file%*/}
    IFS='_' read -ra name <<< "${file%*/}"
    cp -r ../../../template/firefox-template/ template
    docker build -t caballerojavier13/${name[0]}_${name[1]}:${name[2]} .
    docker push caballerojavier13/${name[0]}_${name[1]}:${name[2]}
    rm -rf ./template
    cd ..
  fi;
done