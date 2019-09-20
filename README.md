# SQL Diff

A simple tool that uses a diff of two sql schemas feed via stdin,
to generate `ALTER TABLE` queries to update the database without
having to rebuild the database or had-write the queries.

# Example

To generate the proper the alter statments after a pull:

```bash
git diff master@{1} master <path to sql schemas> | python main.py
```

# Limitations

+ cannot detect changes to a column's name
+ only works inside `CREATE TABLE` statments

# Warning

This is a very simple script written for my personal use. It is
only equipped to solve the problems I faced and I cannot guarantee
it will generate the correct queries in all cases.

DO NOT EXECUTE THE OUTPUT BLINDLY!

# Todo

+ handle more cases
+ write more specific queries e.g. when only changing the default value
+ turn into a module
+ turn into a global cli program


