import pyspark

sc = pyspark.SparkContext('local[*]')

text_file = sc.textFile("GDELT.MASTERREDUCEDV2.TXT")
counts = text_file \
    .map(lambda line: ("line_count", 1)) \
    .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("count.txt")
