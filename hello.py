import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')
print("สวัสดีโลก")
print("สวัสดี Joke")
