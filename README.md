# cwlg-s3-al
Lambda for exporting CloudWatch logs to S3 in a format accepted by Alert Logic as part of a CloudWatch log -> Kinesis Firehose stream implementation. Currently only supports custom log types. Support to be added to support Lambda execution logs if required.

## Environment Variables 
Ensure an environment variable LOG_TYPE with a value of *custom* is set.

Lambda code forked & adapted from https://github.com/CloudSnorkel/CloudWatch2S3