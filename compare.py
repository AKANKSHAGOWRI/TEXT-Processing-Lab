import sys, re, getopt
import glob
import os  # Import os to check the operating system
from nltk.stem import PorterStemmer

opts, args = getopt.getopt(sys.argv[1:], 'hs:pbI:')
opts = dict(opts)

##############################
# HELP option

if '-h' in opts:
    progname = sys.argv[0]
    progname = progname.split('/')[-1]  # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print(help, file=sys.stderr)
    sys.exit()

##############################
# Identify input files, when "-I" option used

if '-I' in opts:
    filenames = glob.glob(opts['-I'])
else:
    # Check the operating system
    if os.name == 'nt':  # Windows
        filenames = glob.glob('NEWS\\*.txt')  # Use backslash for Windows
    else:
        filenames = glob.glob('NEWS/*.txt')  # Use forward slash for other OS

# Check if filenames are being found 
# (comment out after checking)
print('INPUT-FILES:', filenames, file=sys.stderr)

##############################
# STOPLIST option

stops = set()
if '-s' in opts:
    with open(opts['-s'], 'r') as stop_fs:
        for line in stop_fs:
            stops.add(line.strip().lower())  # Convert stop words to lowercase

##############################
# Stemming function

stemmer = PorterStemmer().stem

def stem_word(word):
    return stemmer(word)

##############################
# TOKENIZATION function

def tokenize(text):
    # Use regex to find words, convert to lowercase, and filter out stop words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return [word for word in words if word not in stops]

##############################
# COUNT-WORDS function. 
# Takes 2 inputs: 1= FILE-NAME, 2= stoplist
# Returns a dictionary of word counts

def count_words(filename, stops):
    counts = {}
    with open(filename, 'r') as f:
        text = f.read()
        words = tokenize(text)  # Tokenize the text
        for word in words:
            counts[word] = counts.get(word, 0) + 1  # Count occurrences
    return counts

##############################
# Compute similarity score for document pair
# Inputs are dictionaries of counts for each doc
# Returns similarity score

def jaccard(doc1, doc2):
    set1 = set(doc1.keys())
    set2 = set(doc2.keys())
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if binary:
        # Count-insensitive Jaccard
        return len(intersection) / len(union) if len(union) > 0 else 0
    else:
        # Count-sensitive Jaccard
        numerator = sum(min(doc1.get(word, 0), doc2.get(word, 0)) for word in intersection)
        denominator = sum(max(doc1.get(word, 0), doc2.get(word, 0)) for word in union)
        return numerator / denominator if denominator > 0 else 0

##############################
# Compute counts for individual documents

docs = []

for infile in filenames:
    docs.append(count_words(infile, stops))

##############################
# Compute scores for all document pairs

results = {}
binary = '-b' in opts  # Check if binary option is provided

for i in range(len(docs)-1):
    for j in range(i+1, len(docs)):        
        pair_name = '%s <> %s' % (filenames[i], filenames[j])
        results[pair_name] = jaccard(docs[i], docs[j])

##############################
# Sort, and print top N results

top_N = 20

# Sorting results based on scores
sorted_pairs = sorted(results.items(), key=lambda item: item[1], reverse=True)[:top_N]

# Printing
c = 0
for pair, score in sorted_pairs:
    c += 1
    print('[%d] %s = %.3f' % (c, pair, score), file=sys.stdout)

##############################
import sys, re, getopt
import glob
import os  # Import os to check the operating system
from nltk.stem import PorterStemmer

opts, args = getopt.getopt(sys.argv[1:], 'hs:pbI:')
opts = dict(opts)

##############################
# HELP option

if '-h' in opts:
    progname = sys.argv[0]
    progname = progname.split('/')[-1]  # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print(help, file=sys.stderr)
    sys.exit()

##############################
# Identify input files, when "-I" option used

if '-I' in opts:
    filenames = glob.glob(opts['-I'])
else:
    # Check the operating system
    if os.name == 'nt':  # Windows
        filenames = glob.glob('NEWS\\*.txt')  # Use backslash for Windows
    else:
        filenames = glob.glob('NEWS/*.txt')  # Use forward slash for other OS

# Check if filenames are being found 
# (comment out after checking)
print('INPUT-FILES:', filenames, file=sys.stderr)

##############################
# STOPLIST option

stops = set()
if '-s' in opts:
    with open(opts['-s'], 'r') as stop_fs:
        for line in stop_fs:
            stops.add(line.strip().lower())  # Convert stop words to lowercase

##############################
# Stemming function

stemmer = PorterStemmer().stem

def stem_word(word):
    return stemmer(word)

##############################
# TOKENIZATION function

def tokenize(text):
    # Use regex to find words, convert to lowercase, and filter out stop words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return [word for word in words if word not in stops]

##############################
# COUNT-WORDS function. 
# Takes 2 inputs: 1= FILE-NAME, 2= stoplist
# Returns a dictionary of word counts

def count_words(filename, stops):
    counts = {}
    with open(filename, 'r') as f:
        text = f.read()
        words = tokenize(text)  # Tokenize the text
        for word in words:
            counts[word] = counts.get(word, 0) + 1  # Count occurrences
    return counts

##############################
# Compute similarity score for document pair
# Inputs are dictionaries of counts for each doc
# Returns similarity score

def jaccard(doc1, doc2):
    set1 = set(doc1.keys())
    set2 = set(doc2.keys())
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if binary:
        # Count-insensitive Jaccard
        return len(intersection) / len(union) if len(union) > 0 else 0
    else:
        # Count-sensitive Jaccard
        numerator = sum(min(doc1.get(word, 0), doc2.get(word, 0)) for word in intersection)
        denominator = sum(max(doc1.get(word, 0), doc2.get(word, 0)) for word in union)
        return numerator / denominator if denominator > 0 else 0

##############################
# Compute counts for individual documents

docs = []

for infile in filenames:
    docs.append(count_words(infile, stops))

##############################
# Compute scores for all document pairs

results = {}
binary = '-b' in opts  # Check if binary option is provided

for i in range(len(docs)-1):
    for j in range(i+1, len(docs)):        
        pair_name = '%s <> %s' % (filenames[i], filenames[j])
        results[pair_name] = jaccard(docs[i], docs[j])

##############################
# Sort, and print top N results

top_N = 20

# Sorting results based on scores
sorted_pairs = sorted(results.items(), key=lambda item: item[1], reverse=True)[:top_N]

# Printing
c = 0
for pair, score in sorted_pairs:
    c += 1
    print('[%d] %s = %.3f' % (c, pair, score), file=sys.stdout)

##############################
