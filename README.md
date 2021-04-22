# microSQL - Simple ever SQL DB

## Supported SQL Syntax:
  select cols, ... from table_name [where ...]
  insert into table_name (cols, ...) values (v, ...)
  delete from table_name [where ...]
  create table table_name (cols, ...)
  drop table table_name
  
## Demo
```
>select name, age from hello
  name  age
----------
1 abc   10
2 xyz   15
```

## Available commands:
  | Command | Description |
  | --- | --- |
  | .showdb   | Prints the DB |
  | .help     | Prints this help menu and exits |
  | .exit     | Exits the REPL |
