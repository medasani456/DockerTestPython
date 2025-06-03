from flask import Flask, render_template, request, redirect, send_file
import csv
from collections import defaultdict
import io

app = Flask(__name__)

CSV_FILE = "expenses.csv"

def read_expenses():
    try:
        with open(CSV_FILE, newline='') as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        return []

def write_expenses(rows):
    with open(CSV_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

@app.route("/")
def index():
    expenses = read_expenses()
    return render_template("index.html", expenses=expenses)

@app.route("/add", methods=["POST"])
def add_expense():
    data = [
        request.form["date"],
        request.form["category"],
        request.form["amount"],
        request.form["description"]
    ]
    expenses = read_expenses()
    expenses.append(data)
    write_expenses(expenses)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete_expense(index):
    expenses = read_expenses()
    if 0 <= index < len(expenses):
        del expenses[index]
        write_expenses(expenses)
    return redirect("/")

@app.route("/export")
def export_csv():
    return send_file(CSV_FILE, as_attachment=True)

@app.route("/import", methods=["POST"])
def import_csv():
    file = request.files['file']
    if file:
        content = file.read().decode("utf-8").splitlines()
        reader = csv.reader(content)
        expenses = read_expenses()
        expenses.extend(reader)
        write_expenses(expenses)
    return redirect("/")

@app.route("/chart-data")
def chart_data():
    group_by = request.args.get("group_by", "Category")
    data = defaultdict(float)
    for row in read_expenses():
        key = row[1] if group_by == "Category" else row[0]
        try:
            data[key] += float(row[2])
        except ValueError:
            continue
    return {"labels": list(data.keys()), "values": list(data.values())}

if __name__ == "__main__":
    app.run(debug=True)
