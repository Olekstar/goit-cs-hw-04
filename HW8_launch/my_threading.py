import threading
from collections import defaultdict
import time
import os

def search_in_file(file_path, keywords, result_dict):
    """Search for keywords in a single file and count their occurrences."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
        print(f"Checking file: {file_path}")  # Debug which file is being checked
        for keyword in keywords:
            count = content.count(keyword)
            print(f"Keyword '{keyword}' count in {file_path}: {count}")  # Debug count for each keyword
            if count > 0:
                if keyword in result_dict:
                    result_dict[keyword].append((file_path, count))
                else:
                    result_dict[keyword] = [(file_path, count)]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")

def file_search_thread(file_chunk, keywords, result_dict):
    """Thread function to search for keywords in a chunk of files."""
    for file_path in file_chunk:
        search_in_file(file_path, keywords, result_dict)

def threaded_file_search(files, keywords):
    """Organize files among threads and initiate search, recording keyword counts."""
    num_threads = 4
    threads = []
    result_dict = defaultdict(list)
    file_chunks = [files[i::num_threads] for i in range(num_threads)]

    start_time = time.time()

    for i in range(num_threads):
        thread = threading.Thread(target=file_search_thread, args=(file_chunks[i], keywords, result_dict))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Elapsed time: {time.time() - start_time}s")
    return dict(result_dict)

# Example usage
#directory = os.getcwd()
#files = [f for f in os.listdir(directory) if f.endswith('.txt')]
#keywords = ['born much guess born growth nice', 'born', 'much', 'guess' ]
#results = threaded_file_search(files, keywords)
#print(results)

if __name__ == '__main__':
    directory = os.getcwd()
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    keywords = ['born much guess born growth nice', 'born', 'much', 'guess' ]
    results = threaded_file_search(files, keywords)
    print(results)
