# microSQL - Simple ever SQL DB

## Supported SQL Syntax:
- DDL
```sql
create table table_name (cols, ...)
drop table table_name
```
- DML
```sql
select cols, ... from table_name [where ...]
insert into table_name (cols, ...) values (v, ...)
delete from table_name [where ...]
```
  
## Demo
```sql
>select name, age from demo
┏━━━┳━━━━━━┳━━━━━┓
┃   ┃ name ┃ age ┃
┡━━━╇━━━━━━╇━━━━━┩
│ 1 │ foo  │ 12  │
│ 2 │ bar  │ 16  │
│ 3 │ baz  │ 6   │
└───┴──────┴─────┘
```

## Available commands:
  | Command | Description |
  | --- | --- |
  | .showdb   | Prints the DB |
  | .help     | Prints this help menu and exits |
  | .exit     | Exits the REPL |
  | .debug [on\|off] | Turns debug mode on or off |
  | .db [filename] | Changes db file location |
