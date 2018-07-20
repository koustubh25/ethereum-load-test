FROM python:2-onbuild
ENV RPC_HOST localhost:8545
ENV CSV_BASE_NAME RESULTS
EXPOSE 8089
CMD locust --host $RPC_HOST  --clients $CLIENTS --hatch-rate $HATCH_RATE --no-web --csv-base-name $CSV_BASE_NAME
