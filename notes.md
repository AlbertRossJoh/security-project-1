# General notes
We can log in with
```sql
' or 1=1;--
```

We can get admin credentials when importing notes in the following way.
```sql
0 union select id, username, (SELECT strftime('%Y-%m-%d %H:%M:%S', datetime('now'))), username, 100000 from users
order by id asc;
0 union select id, username, (SELECT strftime('%Y-%m-%d %H:%M:%S', datetime('now'))), password, 100000 from users
order by id asc;
```

We can secure against injection using prepared statements, e.g.
```python
c.execute("SELECT * FROM users WHERE username = ? AND password = ?;", [username, password])
```




# Patches we could implement?

## Password is plaintext
There exist's packages, that can generate hash for us, and make it more secure by that.
for example there exsists this package, that has two functions for this:
```python
from werkzeug.security import generate_password_hash, check_password_hash
```

## The public id of the user's are to predictable.
The user can easily bruteforce the id's through. instead we should use UUID:
```python
import uuid
publicID = str(uuid.uuid4())
```

