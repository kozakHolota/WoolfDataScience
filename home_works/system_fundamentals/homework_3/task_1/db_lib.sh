#!/usr/bin/env bash

run_db() {
    echo "PosgreSQL host (press enter to localhost): "
    read HOST
    echo "Postgres user (press enter to postgres): "
    read USERNAME
    echo "Password: "
    read -s PASSWORD
    echo "PosgreSQL port (press enter to 5432): "
    read PORT

    if [[ ${HOST} = "" ]]
    then
      HOST=localhost
    fi

    if [[ ${USERNAME} = "" ]]
    then
      USERNAME=postgres
    fi

    if [[ ${PORT} = "" ]]
    then
      PORT=5432
    fi

    psql postgresql://${USERNAME}:${PASSWORD}@${HOST}:${PORT} -f $1
}
