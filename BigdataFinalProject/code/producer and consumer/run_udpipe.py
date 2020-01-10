#consumer

import sys
from ufal.udpipe import Model, Pipeline, ProcessingError
from kafka import KafkaConsumer
import json
from pymongo import MongoClient

if sys.version_info[0] < 3:
    import codecs
    import locale
    encoding = locale.getpreferredencoding()
    sys.stdin = codecs.getreader(encoding)(sys.stdin)
    sys.stdout = codecs.getwriter(encoding)(sys.stdout)

if len(sys.argv) < 4:
    sys.stderr.write('Usage: %s input_format(tokenize|conllu|horizontal|vertical) output_format(conllu) model_file\n' % sys.argv[0])
    sys.exit(1)


sys.stderr.write('Loading model: ')
model = Model.load(sys.argv[3])
if not model:
    sys.stderr.write("Cannot load model From file '%s'\n" % sys.argv[3])
    sys.exit(1)
sys.stderr.write('done\n')

pipeline = Pipeline(model, sys.argv[1], Pipeline.DEFAULT, Pipeline.DEFAULT, sys.argv[2])
error = ProcessingError()

conn = MongoClient('127.0.0.1', 27017)
db = conn.Spanish_News
my_set = db.test_set
#my_set.drop()

consumer = KafkaConsumer('Spanish_News', bootstrap_servers=['localhost:9092'])
for content in consumer:
    article = str(content.value.decode("utf-8"))
    a = json.loads(article)
    text = a['text']
    if text is not None:
        processed = pipeline.process(text, error)
        a.update({'UDparse':processed})
        my_set.insert(a)
        if error.occurred():
            sys.stderr.write("An error occurred when running run_udpipe: ")
            sys.stderr.write(error.message)
            sys.stderr.write("\n")
            sys.exit(1)

sys.stdout.write(processed)