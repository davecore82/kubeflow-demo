#!/bin/bash 

exec python /usr/bin/consumer.py &

tensorflow_model_server --port=9000 --rest_api_port=${TF_SERVING_SERVICE_PORT_TF_SERVING_REST} --model_name=${MODEL_NAME} --model_base_path=${MODEL_BASE_PATH} "$@"
