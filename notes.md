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

## Santixization of inputs

Using a package called bleach, should be able to be installed via this command:
pip install bleach
We can sanitize input, to make sure that we do not get malicius code in as a note for example. It removes html code, like \<script\> and other html tags.
It should be used on the log in fields, regiester, and where you make a note, genereally everywhere there is an input.

# Maybe, dont know if we need:

" Missing Cross-Site Request Forgery (CSRF) Protection" no idea what this is, but Chat says we can use Flask-WTF, and import "CSRFProtect", to use this.
