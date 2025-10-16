import pyspark
from time import gmtime, strftime


sc = pyspark.SparkContext('local[*]')

text_file = sc.textFile("GDELT-MINI.TSV")

counts = text_file \
            .map(lambda line: (strftime("%Y%m%d%H%M", gmtime()), 1)) \
            .reduceByKey(lambda a, b: a + b)

counts.first()
