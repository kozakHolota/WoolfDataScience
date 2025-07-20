#!/usr/bin/env bash

log_status() {
  log_file="site_availability.log"
  if [[ "${2}" =~ 200.* ]]
  then
    status="UP"
  else
    status="DOWN"
  fi

  echo "<${1}> is ${status}" >> ${log_file}
}

SITES=(
  "https://google.com"
  "https://facebook.com"
  "https://twitter.com"
  "https://big-bad-pups.com"
)


for website in "${SITES[@]}"
do
  http_status=$(curl -sLi "${website}" | grep -E 'HTTP/.+' | tail -1 | sed 's/HTTP\/[0-9]\.*[0-9]*//')
  log_status ${website} ${http_status}
done