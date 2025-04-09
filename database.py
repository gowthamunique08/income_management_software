from PyQt6.QtSql import QSqlDatabase, QSqlQuery


def init_db(db_name="expenses.db"):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        print("Failed to open the database.")
        return False

    query = QSqlQuery()
    query.exec("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    return True


def fetch_expenses():
    expenses = []
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")

    while query.next():
        expense = [
            query.value(0),  # id
            query.value(1),  # date
            query.value(2),  # category
            query.value(3),  # amount
            query.value(4)   # description
        ]
        expenses.append(expense)

    return expenses


def add_expenses(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    """)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    if not query.exec():
        print("Failed to add expense:", query.lastError().text())
        return False

    return True


def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)

    if not query.exec():
        print("Failed to delete expense:", query.lastError().text())
        return False

    return True
