import csv

def load_csv_file(filename, encoding='utf-8'):

    with open(filename, 'r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        return list(reader)


def apply_filter(data, condition_fn):
 
    return [record for record in data if condition_fn(record)]


def parse_float(value, fallback=0.0):

    try:
        return float(value)
    except ValueError:
        return fallback


def generate_recent_english_content(data):

    for record in data:
        if (record.get('language') == 'English' and
                record.get('type') in ['tvSeries', 'movie'] and
                record.get('endYear', '').isdigit() and
                int(record['endYear']) > 2015):
            yield record

netflix_records = load_csv_file('netflix_list.csv')

high_rated_records = apply_filter(
    netflix_records,
    lambda record: parse_float(record.get('rating', '0')) > 7.5
)

print("Filtered records (Rating > 7.5):")
high_rating_sample = [
    [
        record.get('imdb_id'),
        record.get('title'),
        record.get('rating'),
        record.get('certificate'),
        record.get('startYear')
    ]
    for record in high_rated_records[:5] 
]
for row in high_rating_sample:
    print(row)

print("\nGenerated records (English movies/TV shows ended after 2015):")
english_content_gen = generate_recent_english_content(netflix_records)
for _ in range(5):
    try:
        record = next(english_content_gen)
        print([
            record.get('imdb_id'),
            record.get('title'),
            record.get('language'),
            record.get('type'),
            record.get('endYear')
        ])
    except StopIteration:
        print("No more records available in generator.")
        break

