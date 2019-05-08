"""
This program was adapted from the Stanford NLP class SpamLord homework assignment.
    The code has been rewritten and the data modified, nevertheless
    please do not make this code or the data public.
This base version has no patterns, but has two patterns suggested in comments
    in order to get you started .
"""
import sys
import os
import re
import pprint

"""
TODO
For Part 1 of our assignment, add to these two lists of patterns to match
examples of obscured email addresses and phone numbers in the text.
For optional Part 3, you may need to add other lists of patterns.
"""
# email .edu patterns

# each regular expression pattern should have exactly two sets of parentheses.
#   the first parenthesis should be around the someone part
#   the second parenthesis should be around the somewhere part
#   in an email address whose standard form is someone@somewhere.edu
epatterns = []
# epatterns.append('([A-Za-z]+)@([A-Za-z]+)\.edu')
# BELOW WORKS


# epatterns.append('([A-Za-z0-9._%+-]+)\s*@\s*([A-Za-z0-9.-]+)\.[A-Za-z]')
# epatterns.append('([A-Za-z0-9._%+-]+)\s*(?:@|WHERE)\s*([A-Za-z0-9.-]+)\s*(?:\.|DOM)\s*[A-Za-z]')
epatterns.append('([A-Za-z0-9._%+-]+)\s*(?:@|\s*\bat\b\s*|WHERE)\s*([A-Za-z0-9.-]+)\s*(?:\.|\bdot\b|DOM)\s*[A-Za-z]')
# epatterns.append('E\-?mail\:\s*([A-Za-z0-9._%+-]+)\s*(?:at|AT)\s*([A-Za-z0-9.-]+)\s*(?:(\.|DOT))\s*[A-Za-z]')
epatterns.append('[eE]\-?mail\:?\s*(?:to\s)?(?:\<\/b\>)?\s*([A-Za-z0-9._%+-]+)\s*(?:@|at|AT)\s*([A-Za-z0-9.-]+\s?[A-Za-z0-9.-]*)\s*(?:(\.|DOT|dt|\s))\s*[A-Za-z]')

# FOR JURAFSKY obfuscate('stanford.edu','jurafsky');
epatterns.append('obfuscate\(\'(.+?)\'\,\'(.+?)\'\)')
# epatterns.append('([A-Za-z0-9_%+-]+)\s+at\s+([A-Za-z0-9_%+-]+)\s+([A-Za-z0-9_%+-]+)')
# epatterns.append('email\:(?:\<\/b\>)?\s*([A-Za-z0-9._%+-]+)\s*at\s*(.*)\s*edu')
# epatterns.append('email\:(?:\<\/b\>)?\s*([A-Za-z0-9._%+-]+)\s*at\s*(cs\sdot\sstanford\sdot)\s*edu')

# phone patterns
# each regular expression pattern should have exactly three sets of parentheses.
#   the first parenthesis should be around the area code part XXX
#   the second parenthesis should be around the exchange part YYY
#   the third parenthesis should be around the number part ZZZZ
#   in a phone number whose standard form is XXX-YYY-ZZZZ
ppatterns = []
# # ppatterns.append('(\d{3})-(\d{3})-(\d{4})')
# # ppatterns.append('(\d{3}).(\d{3}).(\d{4})')
# # ppatterns.append('\((\d{3})\)\s(\d{3})-+(\d{4})')
# # # to handle the false positives, we rewrote/refactored two lines above
# ppatterns.append('(\d{3})(?:[-|.]+)(\d{3})(?:[-|.]+)(\d{4})')
# ppatterns.append('\((\d{3})\)\s(\d{3})-+(\d{4})')
# # jurafsky: <small>FAX</small> +1 650 723 5666<br />
# ppatterns.append('(\d{3})\s(\d{3})\s(\d{4})')
# # nass: Phone: [650] 723-5499 
# ppatterns.append('\[(\d{3})\]\s(\d{3})-(\d{4})')




# ppatterns.append('(\d{3})(?:-|.)(\d{3})(?:[-|.]+)(\d{4})')
ppatterns.append('\((\d{3})\)\s(\d{3})-+(\d{4})')
# jurafsky: <small>FAX</small> +1 650 723 5666<br />
# ppatterns.append('(\d{3})\s(\d{3})\s(\d{4})')
# nass: Phone: [650] 723-5499 
ppatterns.append('\[(\d{3})\]\s(\d{3})-(\d{4})')
# OMG FINALLY GETTING RID OF THE FALSE POSITIVES!!
# In order to get rid of the false positives,
# We had to refactor and combine two previous separators 
ppatterns.append('(\d{3})(?:[\W]{1})(\d{3})(?:[\W]{1})(\d{4})')


""" 
This function takes in a filename along with the file object and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

TODO
For Part 3, if you have added other lists, you should add
additional for loops that match the patterns in those lists
and produce correctly formatted results to append to the res list.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        # you may modify the line, using something like substitution
        #    before applyting the patterns
        # To capture emails like die spam pigs
        line = re.sub('\s?\<\!.+?\>\s?', ' ', line)
        # if 'ouster' or 'teresa' in line:
        #     print('ONE +++++++++++++++++++++')
        #     print(line)
        # line = re.sub('\at\s', '@', line)

        # line = re.sub('\sdot\sedu', '', line)
        line = re.sub('\&\w+\;', '', line)
        line = re.sub('\s*dot|DOT|dt\.?\s*', '.', line)

        # To capture emails like this: 
        # latombe<del>@cs.stanford.edu
        line = re.sub('\<del\>', '', line)

        # To capture emails like this:
        # ada&#x40;graphics.stanford.edu
        line = re.sub('&#x40;', '@', line)
        line = re.sub('&lt;', '', line)

        # To capture emails like this:
        # manning <at symbol> cs.stanford.edu
        line = re.sub('\<at\ssymbol\>', '@', line)

        # To capture emails like this:
        # (followed by &ldquo;@cs.stanford.edu&rdquo;)
        line = re.sub('\s\(followed.+?\@', '@', line)

        # To capture emails like 
        # jks at robotics;stanford;edu
        line = re.sub(';', '.', line)

        line = re.sub('[sS]erver', '    ', line)
        if 'edu' in line:
            line = re.sub('\s+at\s+', '@', line)

        line = re.sub('\.\s+', '.', line)

        if '-@-' in line:
            line = re.sub('-', '', line)

        if 'pal' in line:
            print('TWO +++++++++++++++++++++')
            line = re.sub('(?<=@)@(\s)', '.', line)
            print(line)
        
        # email pattern list
        for epat in epatterns:
            # each epat has 2 sets of parentheses so each match will have 2 items in a list
            matches = re.findall(epat,line)
            for m in matches:
                print('MATCHES++++++++++++++++++++++++')
                print(m)
                print(m[0])

                
                # string formatting operator % takes elements of list m
                #   and inserts them in place of each %s in the result string
                # email has form  someone@somewhere.edu
                #email = '%s@%s.edu' % m


                # To capture emails matched above with multiple ..
                # uma@cs..stanford.edu
                somewhere = re.sub('\.+', '.', m[1])
                
                # To capture emails matched above with spaces like this: 
                # pal@cs stanford.edu
                somewhere = re.sub('\s+', '.', m[1])

                # To capture emails matched above with periods like this: 
                # serafim@cs.stanford..edu
                somewhere = somewhere.rstrip('.')

                # To capture emails that are .com instead of .edu
                # very hacky I know

                someone = '' if 'Server' in m[0] else m[0]
                # To capture someones with multiple ..
                # mid..zelenski@cs.stanford.edu
                someone = re.sub('\.+', '.', someone)

                if '.edu' in m[0]:
                    name = m[1]
                    email = m[0]
                    someone = name
                    somewhere = email.split('.')[0]
                edu = 'com' if 'gradiance' in m[1] else 'edu'
                email = '{}@{}.{}'.format(someone,somewhere, edu)
                res.append((name,'e',email))

        # phone pattern list
        for ppat in ppatterns:
            # each ppat has 3 sets of parentheses so each match will have 3 items in a list
            matches = re.findall(ppat,line)
            for m in matches:
                # phone number has form  areacode-exchange-number
                #phone = '%s-%s-%s' % m
                phone = '{}-{}-{}'.format(m[0],m[1],m[2])
                res.append((name,'p',phone))
    return res

"""
You should not edit this function.
"""
def process_dir(data_path):
    # save complete list of candidates
    guess_list = []
    # save list of filenames
    fname_list = []

    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        fname_list.append(fname)
        path = os.path.join(data_path,fname)
        f = open(path,'r', encoding='latin-1')
        # get all the candidates for this file
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list, fname_list

"""
You should not edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r', encoding='latin-1')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not edit this function.
Given a list of guessed contacts and gold contacts, this function
    computes the intersection and set differences, to compute the true
    positives, false positives and false negatives. 
It also takes a dictionary that gives the guesses for each filename, 
    which can be used for information about false positives. 
Importantly, it converts all of the values to lower case before comparing.
"""
def score(guess_list, gold_list, fname_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    # for each file name, put the golds from that file in a dict
    gold_dict = {}
    for fname in fname_list:
        gold_dict[fname] = [gold for gold in gold_list if fname == gold[0]]

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)

    print ('True Positives (%d): ' % len(tp))
    # print all true positives
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    # for each false positive, print it and the list of gold for debugging
    for item in fp:
        fp_name = item[0]
        pp.pprint(item)
        fp_list = gold_dict[fp_name]
        for gold in fp_list:
            s = pprint.pformat(gold)
            print('   gold: ', s)
    print ('False Negatives (%d): ' % len(fn))
    # print all false negatives
    pp.pprint(fn)
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not edit this function.
It takes in the string path to the data directory and the gold file
"""
def main(data_path, gold_path):
    guess_list, fname_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list, fname_list)

"""
commandline interface assumes that you are in the directory containing "data" folder
It then processes each file within that data folder and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    print ('Assuming ContactFinder.py called in directory with data folder')
    main('data/dev', 'data/devGOLD')
