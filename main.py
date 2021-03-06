import pickle
import operator
from typing import Any
from rich.console import Console
from rich.table import Table

DEBUG = False
DB_FILE = 'microsql.db'

db = dict()
console = Console()

op_map = {'==': operator.eq, '!=': operator.ne, '>': operator.gt,
          '<': operator.lt, '>=': operator.ge, '<=': operator.le}


def main():
    load_from_db()

    while True:
        match input(">").split():
            case [".exit"]:
                break
            case [".help"]:
                print_help()
                break
            case [".showdb"]:
                console.print(db)
            case [".debug", ("on" | "off") as d]:
                global DEBUG
                DEBUG = (d == "on")
            case [".db", filename]:
                global DB_FILE
                DB_FILE = filename
            case [cmd, *rest]:
                try:
                    eval_cmd(cmd, *rest)
                except:
                    console.print_exception()

    persist_to_db()


def eval_cmd(cmd: str, *rest):
    match cmd:
        case "select":
            cols, rest = ' '.join(rest).split(' from ')

            cols = parse_csv(cols)
            printd("cols =", cols)

            table_name, *rest = rest.split()
            printd("table =", table_name)

            data = get_data_from_table(table_name, cols)

            if rest:
                clause, *rest = rest
                printd("clause =", clause)

                if clause == "where":
                    lhs, op, rhs = rest
                    # TODO: check schema if lhs (col name) exists
                    # and rhs is of correct type
                    op_f = op_map[op]
                    table = [e for e in data if op_f(
                        e[lhs], parse_literal(rhs))]
                    print_table(table)
            else:
                print_table(data)
        case "insert":
            _into, table_name, *rest = ' '.join(rest).split()
            printd("table =", table_name, rest)

            cols, row_data = ' '.join(rest).split(" values ")
            cols = parse_csv(cols[1:-1])
            row_data = parse_csv(row_data[1:-1])
            row_data = list(map(parse_literal, row_data))
            data = dict(zip(cols, row_data))
            printd("data =", data)

            insert_row_into_table(table_name, data)
        case "delete":
            _from, table_name, *rest = ' '.join(rest).split()
            printd("table =", table_name)
            print(rest)
            clause, *rest = rest
            printd("filter =", clause)

            if clause == "where":
                lhs, op, rhs = rest
                delete_row_from_table(
                    table_name, op_map[op], lhs, parse_literal(rhs))
        case "create":
            _table, table_name, *rest = ' '.join(rest).split()
            printd("table =", table_name)

            cols = parse_csv(' '.join(rest)[1:-1])
            printd("cols =", cols)

            create_table(table_name, cols)
        case "drop":
            _table, table_name = ' '.join(rest).split()
            printd("table =", table_name)

            delete_table(table_name)


def get_data_from_table(table_name: str, cols: list[str]):
    return [{k: d[k] for k in cols} for d in db[table_name]]


def insert_row_into_table(table_name: str, data: dict[str, Any]):
    db[table_name].append(data)


def delete_row_from_table(table_name: str, f, lhs, rhs):
    d = 0
    for row in db[table_name]:
        if f(row[lhs], rhs):
            db[table_name].remove(row)
            d += 1
    print("Deleted %d rows" % d)


def create_table(table_name: str, cols: list[str]):
    db[table_name] = []


def delete_table(table_name: str):
    del db[table_name]


def load_from_db():
    global db
    try:
        with open(DB_FILE, 'rb') as db_file:
            db = pickle.load(db_file)
    except FileNotFoundError:
        pass


def persist_to_db():
    with open(DB_FILE, 'wb') as db_file:
        pickle.dump(db, db_file)


def parse_csv(csv):
    return csv.replace(' ', '').split(',')


def parse_literal(literal):
    try:
        return int(literal)
    except ValueError:
        return str(literal)[1:-1]


def print_table(dataset: dict[str, Any]):
    vals = [d.values() for d in dataset]

    table = Table("", *dict.fromkeys(dataset[0]))
    for i, v in enumerate(vals):
        table.add_row(str(i+1), *map(str, v))

    console.print(table)


def printd(*args):
    if DEBUG:
        console.print(*args, style="red")


def print_help():
    print("""
  microSQL is a simple ever SQL DB.

  Supported SQL Syntax:
    select cols, ... from table_name [where ...]
    insert into table_name (cols, ...) values (v, ...)
    delete from table_name [where ...]
    create table table_name (cols, ...)
    drop table table_name

  Available commands:
    .showdb      Prints the DB
    .help        Prints this help menu and exits
    .exit        Exits the REPL
  """)


if __name__ == "__main__":
    main()
