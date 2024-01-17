# sqlite-concurrent-writes-investigation

This repo is my investigation into a SQLite database's ability to handle concurrent reads and writes. 

Conclusion: it is performant and flawless. 

You can run the test yourself like this:

```bash
# create SQLite database and a table in it
python init_db.py

# do 1000 write operations
python load_test.py -n 1000 -w

# do 1000 read operations
python load_test.py -n 1000 -r

# do 1000 read and write operations intermingled
python load_test.py -n 1000 -w -r

# view all of the rows created in the database
python view_whole_table.py 

# delete SQLite database #
python clean_up.py
```
