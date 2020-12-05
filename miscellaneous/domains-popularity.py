import collections
domains_length = [len(span.find('a').getText()) - 1 for span in spans]

counter = collections.Counter(domains_length)
for key, value in counter.iteritems():
    print key, value
