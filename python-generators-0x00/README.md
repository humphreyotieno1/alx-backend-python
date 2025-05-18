# Python Generators Project

This project focuses on implementing and using Python generators for efficient data processing, particularly when dealing with large datasets in a SQL database environment.

## Overview

Python generators allow you to create iterators in a simple way, producing items one at a time and only when needed. This is extremely useful for memory management when working with large datasets.

## Project Tasks

### 0. Getting Started with Python Generators

**Objective**: Set up a MySQL database and populate it with sample data.

**File**: `seed.py`

**Requirements**:
- Connect to MySQL database server
- Create a database named `ALX_prodev`
- Create a table `user_data` with fields:
    - `user_id` (Primary Key, UUID, Indexed)
    - `name` (VARCHAR, NOT NULL)
    - `email` (VARCHAR, NOT NULL)
    - `age` (DECIMAL, NOT NULL)
- Populate the database with sample data from `user_data.csv`

**Functions to implement**:
- `connect_db()`: Connects to the MySQL database server
- `create_database(connection)`: Creates the database if it doesn't exist
- `connect_to_prodev()`: Connects to the ALX_prodev database
- `create_table(connection)`: Creates the user_data table if it doesn't exist
- `insert_data(connection, data)`: Inserts data into the database if it doesn't exist

### 1. Generator that Streams Rows from an SQL Database

**Objective**: Create a generator to stream rows from the SQL database one by one.

**File**: `0-stream_users.py`

**Requirements**:
- Implement a function `stream_users()` that yields rows one by one
- Use the `yield` keyword to create a generator
- The function should have no more than 1 loop
- Each yielded row should be a dictionary with keys matching the table fields

### 2. Batch Processing Large Data

**Objective**: Create a generator to fetch and process data in batches.

**File**: `1-batch_processing.py`

**Requirements**:
- Implement `stream_users_in_batches(batch_size)` to fetch rows in batches
- Implement `batch_processing(batch_size)` to filter users over the age of 25
- Use no more than 3 loops in your code
- Use the `yield` generator

### 3. Lazy Loading Paginated Data

**Objective**: Simulate fetching paginated data from the database using lazy loading.

**File**: `2-lazy_paginate.py`

**Requirements**:
- Implement a generator function `lazy_paginate(page_size)` that uses the provided `paginate_users(page_size, offset)` function
- Only fetch the next page when needed, starting with an offset of 0
- Use only one loop
- Use the `yield` generator

### 4. Memory-Efficient Aggregation with Generators

**Objective**: Use a generator to compute an aggregate function (average age) for a large dataset efficiently.

**File**: `4-stream_ages.py`

**Requirements**:
- Implement a generator `stream_user_ages()` that yields user ages one by one
- Use this generator to calculate the average age without loading the entire dataset
- Print "Average age of users: [average age]"
- Use no more than two loops
- Do not use SQL AVERAGE function

## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/your-username/alx-backend-python.git
```

2. Navigate to the project directory:
```
cd alx-backend-python/python-generators-0x00
```

3. Install required dependencies:
```
pip install mysql-connector-python
```

4. Ensure MySQL is installed and running on your system

## Usage

Execute each task file with the corresponding main file to test the functionality.

For example:
```
python 1-main.py
```

## Requirements

- Python 3.7+
- MySQL server
- mysql-connector-python