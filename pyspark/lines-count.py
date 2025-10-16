import pyspark
sc = pyspark.SparkContext('local[*]')

text_file = sc.textFile("GDELT-MINI.TSV")
text_file.count()
