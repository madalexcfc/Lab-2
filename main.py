import csv
import random
import xml.etree.ElementTree as ET

BOOKS_CSV_PATH = 'C:/Users/PC/Desktop/test/Lab-2/Lab-2/books.csv'
CURRENCY_XML_PATH = 'C:/Users/PC/Desktop/test/Lab-2/Lab-2/currency.xml'
OUTPUT_BIBLIOGRAPHY_PATH = 'C:/Users/PC/Desktop/test/Lab-2/Lab-2/bibliography.txt'

def count_long_titles(csv_path, length=30):
    with open(csv_path, encoding='windows-1251') as file:
        reader = csv.DictReader(file, delimiter=';')
        count = sum(1 for row in reader if len(row['Название']) > length)
    return count

def search_books_by_author(csv_path, author, limit=10):
    results = []
    with open(csv_path, encoding='windows-1251') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if author.lower() in row['Автор'].lower():
                results.append(row)
            if len(results) >= limit:
                break
    return results

def generate_bibliography(csv_path, output_path, count=20):
    with open(csv_path, encoding='windows-1251') as file:
        reader = csv.DictReader(file, delimiter=';')
        rows = list(reader)
        selected_rows = random.sample(rows, min(count, len(rows)))

    with open(output_path, 'w', encoding='windows-1251') as file:
        for i, row in enumerate(selected_rows, start=1):
            file.write(f"{i}. {row['Автор']}. {row['Название']} - {row['Дата поступления']}\n")

def parse_currency_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    currencies = []
    for currency in root.findall('.//Valute'):
        code = currency.find('CharCode').text
        name = currency.find('Name').text
        value = float(currency.find('Value').text.replace(',', '.'))
        currencies.append({'code': code, 'name': name, 'value': value})
    return currencies

if __name__ == '__main__':
    long_titles_count = count_long_titles(BOOKS_CSV_PATH)
    print(f"Количество записей с названием длиннее 30 символов: {long_titles_count}")

    author_query = input("Введите имя автора для поиска: ")
    found_books = search_books_by_author(BOOKS_CSV_PATH, author_query)
    print("Найденные книги:")
    for book in found_books:
        print(f"{book['Автор']} - {book['Название']} ({book['Дата поступления']})")

    generate_bibliography(BOOKS_CSV_PATH, OUTPUT_BIBLIOGRAPHY_PATH)
    print(f"Библиография сохранена в файл {OUTPUT_BIBLIOGRAPHY_PATH}")

    currencies = parse_currency_xml(CURRENCY_XML_PATH)
    print("Извлеченные данные:")
    for currency in currencies:
        print(f"{currency['code']}: {currency['name']} - {currency['value']} RUB")
