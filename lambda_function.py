import base64
import gzip
import json
import os
from datetime import datetime

logType = os.environ['LOG_TYPE']


def handle_records(records):
    for record in records:
        record_id = record["recordId"]
        data = json.loads(gzip.decompress(base64.b64decode(record["data"])))
        # Handle different accepted log types
        # Creates single line log messages with the following format: Custom CloudWatch Log Record: [ISO 8601 timestamp] - Log Message
        if logType == 'custom':
            nl = '\n\n'
            outputData = base64.b64encode(
                "".join(
                    f"Custom CloudWatch Log Record: [{datetime.fromtimestamp(e['timestamp']/1000).isoformat(timespec='milliseconds')}] - {e['message']}".join(
                        nl)
                    for e in data["logEvents"]
                ).encode("utf-8")
            ).decode("utf-8")

        # TODO: Implement support for Lambda logs

        if data["messageType"] == "CONTROL_MESSAGE":
            yield {
                "result": "Dropped",
                "recordId": record_id
            }
        elif data["messageType"] == "DATA_MESSAGE":
            yield {
                "recordId": record_id,
                "result": "Ok",
                "data": outputData
            }
        else:
            yield {
                "result": "ProcessingFailed",
                "recordId": record_id
            }


def handler(event, context):
    result = []
    size = 0

    for record in handle_records(event["records"]):
        size += len(str(record))
        if size < 6000000:
            # lambda limits output to 6mb
            # kinesis will treat records not here as failed and retry
            # TODO or do we need to reingest?
            result.append(record)
        else:
            break
    print(result)
    return {"records": result}
