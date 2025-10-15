from luigi.s3 import S3Client
from boto.requestlog import RequestLogger


s = S3Client()

# s.s3.set_request_hook(RequestLogger())

s.get('s3://ahiwdtdjlrqzhwssvvlslfut/LargeValidJsonString.json', './example.json')
