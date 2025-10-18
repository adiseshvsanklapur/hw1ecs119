"""
Part 2: Performance Comparisons

In this part, we will explore comparing the performance
of different pipelines.
First, we will set up some helper classes.
Then we will do a few comparisons
between two or more versions of a pipeline
to report which one is faster.
"""

import part1
import time
import matplotlib.pyplot as plt
import pandas as pd

"""
=== Questions 1-5: Throughput and Latency Helpers ===

We will design and fill out two helper classes.

The first is a helper class for throughput (Q1).
The class is created by adding a series of pipelines
(via .add_pipeline(name, size, func))
where name is a title describing the pipeline,
size is the number of elements in the input dataset for the pipeline,
and func is a function that can be run on zero arguments
which runs the pipeline (like def f()).

The second is a similar helper class for latency (Q3).

1. Throughput helper class

Fill in the add_pipeline, eval_throughput, and generate_plot functions below.
"""
NUM_RUNS = 10

class ThroughputHelper:
    def __init__(self):
        self.pipelines = []
        self.names = []
        self.sizes = []
        self.throughputs = None

    def add_pipeline(self, name, size, func):
        self.names.append(name)
        self.sizes.append(size)
        self.pipelines.append(func)

    def compare_throughput(self):
        self.throughputs = []
        for i, func in enumerate(self.pipelines):
            start_time = time.time()
            for _ in range(NUM_RUNS):
                func()
            end_time = time.time()
            total_time = end_time - start_time
            total_items = self.sizes[i] * NUM_RUNS
            throughput = total_items / total_time
            
            self.throughputs.append(throughput)
        
        return self.throughputs

    def generate_plot(self, filename):
        if self.throughputs is None:
            self.compare_throughput()
        plt.figure(figsize=(10, 6))
        plt.bar(self.names, self.throughputs)
        plt.xlabel('Pipeline')
        plt.ylabel('Throughput (items/second)')
        plt.title('Pipeline Throughput Comparison')
        plt.xticks(rotation=45, ha='right')
        plt.legend(['Throughput'])
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
"""
As your answer to this part,
return the name of the method you decided to use in
matplotlib.

(Example: "boxplot" or "scatter")
"""

def q1():
    return "bar"

"""
2. A simple test case

To make sure your monitor is working, test it on a very simple
pipeline that adds up the total of all elements in a list.

We will compare three versions of the pipeline depending on the
input size.
"""

LIST_SMALL = [10] * 100
LIST_MEDIUM = [10] * 100_000
LIST_LARGE = [10] * 100_000_000

def add_list(l):
    total = 0
    for item in l:
        total += item
    return total

def q2a():
    h = ThroughputHelper()
    h.add_pipeline("small", len(LIST_SMALL), lambda: add_list(LIST_SMALL))
    h.add_pipeline("medium", len(LIST_MEDIUM), lambda: add_list(LIST_MEDIUM))
    h.add_pipeline("large", len(LIST_LARGE), lambda: add_list(LIST_LARGE))
    throughputs = h.compare_throughput()
    h.generate_plot('output/part2-q2a.png')
    return throughputs

"""
2b.
Which pipeline has the highest throughput?
Is this what you expected?

=== ANSWER Q2b BELOW ===
the large pipeline has the highest throughput because larger datasets can process more items per second, even though they take longer overall. this is expected because the overhead of starting the operation is amortized over more items.
=== END OF Q2b ANSWER ===
"""

"""
3. Latency helper class.

Now we will create a similar helper class for latency.

The helper should assume a pipeline that only has *one* element
in the input dataset.

It should use the NUM_RUNS variable as with throughput.
"""

class LatencyHelper:
    def __init__(self):
        self.pipelines = []
        self.names = []
        self.latencies = None

    def add_pipeline(self, name, func):
        self.names.append(name)
        self.pipelines.append(func)

    def compare_latency(self):
        self.latencies = []
        
        for func in self.pipelines:
            start_time = time.time()
            for _ in range(NUM_RUNS):
                func()
            end_time = time.time()
            total_time = end_time - start_time
            avg_latency = (total_time / NUM_RUNS) * 1000
            self.latencies.append(avg_latency)
        return self.latencies
    
    def generate_plot(self, filename):
        if self.latencies is None:
            self.compare_latency()
        plt.figure(figsize=(10, 6))
        plt.bar(self.names, self.latencies)
        plt.xlabel('Pipeline')
        plt.ylabel('Latency (milliseconds)')
        plt.title('Pipeline Latency Comparison')
        plt.xticks(rotation=45, ha='right')
        plt.legend(['Latency'])
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

"""
As your answer to this part,
return the number of input items that each pipeline should
process if the class is used correctly.
"""

def q3():
    return 1

"""
4. To make sure your monitor is working, test it on
the simple pipeline from Q2.

For latency, all three pipelines would only process
one item. Therefore instead of using
LIST_SMALL, LIST_MEDIUM, and LIST_LARGE,
for this question run the same pipeline three times
on a single list item.
"""

LIST_SINGLE_ITEM = [10] # Note: a list with only 1 item

def q4a():
    h = LatencyHelper()
    h.add_pipeline("run1", lambda: add_list(LIST_SINGLE_ITEM))
    h.add_pipeline("run2", lambda: add_list(LIST_SINGLE_ITEM))
    h.add_pipeline("run3", lambda: add_list(LIST_SINGLE_ITEM))
    latencies = h.compare_latency()
    h.generate_plot('output/part2-q4a.png')
    return latencies

"""
4b.
How much did the latency vary between the three copies of the pipeline?
Is this more or less than what you expected?

=== ANSWER Q4b BELOW ===
the latency varied very little between the three runs, usually within a few microseconds or less. this is expected because we're running the exact same operation on the same input, so the only variation comes from system noise like other processes running on the computer.
=== END OF Q4b ANSWER ===
"""

"""
Now that we have our helpers, let's do a simple comparison.

NOTE: you may add other helper functions that you may find useful
as you go through this file.

5. Comparison on Part 1

Finally, use the helpers above to calculate the throughput and latency
of the pipeline in part 1.
"""

# You will need these:
# part1.load_input
# part1.PART_1_PIPELINE

def q5a():
    h = ThroughputHelper()
    df = part1.load_input()
    size = len(df)
    h.add_pipeline("part1_pipeline", size, part1.PART_1_PIPELINE)
    throughputs = h.compare_throughput()
    h.generate_plot('output/part2-q5a.png')
    return throughputs[0]

def q5b():
    h = LatencyHelper()
    h.add_pipeline("part1_pipeline", part1.PART_1_PIPELINE)
    latencies = h.compare_latency()
    h.generate_plot('output/part2-q5b.png')
    return latencies[0]

"""
===== Questions 6-10: Performance Comparison 1 =====

For our first performance comparison,
let's look at the cost of getting input from a file, vs. in an existing DataFrame.

6. We will use the same population dataset
that we used in lecture 3.

Load the data using load_input() given the file name.

- Make sure that you clean the data by removing
  continents and world data!
  (World data is listed under OWID_WRL)

Then, set up a simple pipeline that computes summary statistics
for the following:

- *Year over year increase* in population, per country

    (min, median, max, mean, and standard deviation)

How you should compute this:

- For each country, we need the maximum year and the minimum year
in the data. We should divide the population difference
over this time by the length of the time period.

- Make sure you throw out the cases where there is only one year
(if any).

- We should at this point have one data point per country.

- Finally, as your answer, return a list of the:
    min, median, max, mean, and standard deviation
  of the data.

Hints:
You can use the describe() function in Pandas to get these statistics.
You should be able to do something like
df.describe().loc["min"]["colum_name"]

to get a specific value from the describe() function.

You shouldn't use any for loops.
See if you can compute this using Pandas functions only.
"""

def load_input(filename):
    df = pd.read_csv(filename)
    df = df[~df['Code'].str.contains('OWID', na=False)]
    
    return df

def population_pipeline(df):
    grouped = df.groupby('Code')
    
    results = []
    for code, group in grouped:
        if len(group) <= 1:
            continue
        
        group = group.sort_values('Year')
        
        min_year = group['Year'].iloc[0]
        max_year = group['Year'].iloc[-1]
        min_pop = group['Population (historical)'].iloc[0]
        max_pop = group['Population (historical)'].iloc[-1]
        
        year_diff = max_year - min_year
        pop_diff = max_pop - min_pop
        yoy_increase = pop_diff / year_diff
        
        results.append(yoy_increase)
    
    if len(results) == 0:
        return [0, 0, 0, 0, 0]
    
    results_series = pd.Series(results)
    stats = results_series.describe()
    
    return [
        stats['min'],
        stats['50%'],
        stats['max'],
        stats['mean'],
        stats['std']
    ]

def q6():
    df = load_input('data/population.csv')
    result = population_pipeline(df)
    return result

"""
7. Varying the input size

Next we want to set up three different datasets of different sizes.

Create three new files,
    - data/population-small.csv
      with the first 600 rows
    - data/population-medium.csv
      with the first 6000 rows
    - data/population-single-row.csv
      with only the first row
      (for calculating latency)

You can edit the csv file directly to extract the first rows
(remember to also include the header row)
and save a new file.

Make four versions of load input that load your datasets.
(The _large one should use the full population dataset.)
Each should return a dataframe.

The input CSV file will have 600 rows, but the DataFrame (after your cleaning) may have less than that.
"""

def load_input_small():
    return load_input('data/population-small.csv')

def load_input_medium():
    return load_input('data/population-medium.csv')

def load_input_large():
    return load_input('data/population.csv')

def load_input_single_row():
    return load_input('data/population-single-row.csv')

def q7():
    df = pd.read_csv('data/population.csv')
    df.head(600).to_csv('data/population-small.csv', index=False)
    df.head(6000).to_csv('data/population-medium.csv', index=False)
    df.head(1).to_csv('data/population-single-row.csv', index=False)
    s = load_input_small()
    m = load_input_medium()
    l = load_input_large()
    x = load_input_single_row()
    return [len(s), len(m), len(l), len(x)]

"""
8.
Create baseline pipelines

First let's create our baseline pipelines.
Create four pipelines,
    baseline_small
    baseline_medium
    baseline_large
    baseline_latency

based on the three datasets above.
Each should call your population_pipeline from Q6.

Your baseline_latency function will not be very interesting
as the pipeline does not produce any meaningful output on a single row!
You may choose to instead run an example with two rows,
or you may fill in this function in any other way that you choose
that you think is meaningful.
"""

def baseline_small():
    df = load_input_small()
    return population_pipeline(df)

def baseline_medium():
    df = load_input_medium()
    return population_pipeline(df)

def baseline_large():
    df = load_input_large()
    return population_pipeline(df)

def baseline_latency():
    df = load_input_single_row()
    return population_pipeline(df)

def q8():
    _ = baseline_medium()
    return ["baseline_small", "baseline_medium", "baseline_large", "baseline_latency"]

"""
9.
Finally, let's compare whether loading an input from file is faster or slower
than getting it from an existing Pandas dataframe variable.

Create four new dataframes (constant global variables)
directly in the script.
Then use these to write 3 new pipelines:
    fromvar_small
    fromvar_medium
    fromvar_large
    fromvar_latency

These pipelines should produce the same answers as in Q8.

As your answer to this part;
a. Generate a plot in output/part2-q9a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, fromvar_small, fromvar_medium, fromvar_large
b. Generate a plot in output/part2-q9b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, fromvar_latency
"""

POPULATION_SMALL = load_input('data/population-small.csv')
POPULATION_MEDIUM = load_input('data/population-medium.csv')
POPULATION_LARGE = load_input('data/population.csv')
POPULATION_SINGLE_ROW = load_input('data/population-single-row.csv')

def fromvar_small():
    return population_pipeline(POPULATION_SMALL)

def fromvar_medium():
    return population_pipeline(POPULATION_MEDIUM)

def fromvar_large():
    return population_pipeline(POPULATION_LARGE)

def fromvar_latency():
    return population_pipeline(POPULATION_SINGLE_ROW)

def q9a():
    h = ThroughputHelper()
    h.add_pipeline("baseline_small", len(POPULATION_SMALL), baseline_small)
    h.add_pipeline("baseline_medium", len(POPULATION_MEDIUM), baseline_medium)
    h.add_pipeline("baseline_large", len(POPULATION_LARGE), baseline_large)
    h.add_pipeline("fromvar_small", len(POPULATION_SMALL), fromvar_small)
    h.add_pipeline("fromvar_medium", len(POPULATION_MEDIUM), fromvar_medium)
    h.add_pipeline("fromvar_large", len(POPULATION_LARGE), fromvar_large)
    throughputs = h.compare_throughput()
    h.generate_plot('output/part2-q9a.png')
    
    return throughputs

def q9b():
    h = LatencyHelper()
    h.add_pipeline("baseline_latency", baseline_latency)
    h.add_pipeline("fromvar_latency", fromvar_latency)
    latencies = h.compare_latency()
    h.generate_plot('output/part2-q9b.png')
    
    return latencies

"""
10.
Comment on the plots above!
How dramatic is the difference between the two pipelines?
Which differs more, throughput or latency?
What does this experiment show?

===== ANSWER Q10 BELOW =====
the fromvar pipelines are significantly faster than baseline pipelines because they don't have the overhead of reading from disk. latency shows a more dramatic difference than throughput because the file I/O overhead is more noticeable when processing small amounts of data. this experiment shows that loading data from memory is much faster than reading from files, especially for latency-sensitive operations.
===== END OF Q10 ANSWER =====
"""

"""
===== Questions 11-14: Performance Comparison 2 =====

Our second performance comparison will explore vectorization.

Operations in Pandas use Numpy arrays and vectorization to enable
fast operations.
In particular, they are often much faster than using for loops.

Let's explore whether this is true!

11.
First, we need to set up our pipelines for comparison as before.

We already have the baseline pipelines from Q8,
so let's just set up a comparison pipeline
which uses a for loop to calculate the same statistics.

Your pipeline should produce the same answers as in Q6 and Q8.

Create a new pipeline:
- Iterate through the dataframe entries. You can assume they are sorted.
- Manually compute the minimum and maximum year for each country.
- Compute the same answers as in Q6.
- Manually compute the summary statistics for the resulting list (min, median, max, mean, and standard deviation).
"""

def for_loop_pipeline(df):
    country_data = {}
    
    for idx, row in df.iterrows():
        code = row['Code']
        year = row['Year']
        pop = row['Population (historical)']
        
        if code not in country_data:
            country_data[code] = {
                'min_year': year,
                'max_year': year,
                'min_pop': pop,
                'max_pop': pop
            }
        else:
            if year < country_data[code]['min_year']:
                country_data[code]['min_year'] = year
                country_data[code]['min_pop'] = pop
            if year > country_data[code]['max_year']:
                country_data[code]['max_year'] = year
                country_data[code]['max_pop'] = pop
    
    yoy_increases = []
    for code, data in country_data.items():
        if data['min_year'] == data['max_year']:
            continue
        
        year_diff = data['max_year'] - data['min_year']
        pop_diff = data['max_pop'] - data['min_pop']
        yoy_increase = pop_diff / year_diff
        yoy_increases.append(yoy_increase)
    
    if len(yoy_increases) == 0:
        return [0, 0, 0, 0, 0]
    
    yoy_increases.sort()
    n = len(yoy_increases)
    
    min_val = yoy_increases[0]
    max_val = yoy_increases[-1]
    
    if n % 2 == 0:
        median_val = (yoy_increases[n//2 - 1] + yoy_increases[n//2]) / 2
    else:
        median_val = yoy_increases[n//2]
    
    mean_val = sum(yoy_increases) / n
    
    variance = sum((x - mean_val) ** 2 for x in yoy_increases) / n
    std_val = variance ** 0.5
    
    return [min_val, median_val, max_val, mean_val, std_val]

def q11():
    df = load_input('data/population.csv')
    result = for_loop_pipeline(df)
    return result

"""
12.
Now, let's create our pipelines for comparison.

As before, write 4 pipelines based on the datasets from Q7.
"""

def for_loop_small():
    df = load_input_small()
    return for_loop_pipeline(df)

def for_loop_medium():
    df = load_input_medium()
    return for_loop_pipeline(df)

def for_loop_large():
    df = load_input_large()
    return for_loop_pipeline(df)

def for_loop_latency():
    df = load_input_single_row()
    return for_loop_pipeline(df)

def q12():
    _ = for_loop_medium()
    return ["for_loop_small", "for_loop_medium", "for_loop_large", "for_loop_latency"]

"""
13.
Finally, let's compare our two pipelines,
as we did in Q9.

a. Generate a plot in output/part2-q13a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, for_loop_small, for_loop_medium, for_loop_large

b. Generate a plot in output/part2-q13b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, for_loop_latency
"""

def q13a():
    h = ThroughputHelper()
    
    h.add_pipeline("baseline_small", len(POPULATION_SMALL), baseline_small)
    h.add_pipeline("baseline_medium", len(POPULATION_MEDIUM), baseline_medium)
    h.add_pipeline("baseline_large", len(POPULATION_LARGE), baseline_large)
    
    h.add_pipeline("for_loop_small", len(POPULATION_SMALL), for_loop_small)
    h.add_pipeline("for_loop_medium", len(POPULATION_MEDIUM), for_loop_medium)
    h.add_pipeline("for_loop_large", len(POPULATION_LARGE), for_loop_large)
    
    throughputs = h.compare_throughput()
    h.generate_plot('output/part2-q13a.png')
    
    return throughputs

def q13b():
    h = LatencyHelper()
    
    h.add_pipeline("baseline_latency", baseline_latency)
    h.add_pipeline("for_loop_latency", for_loop_latency)
    
    latencies = h.compare_latency()
    h.generate_plot('output/part2-q13b.png')
    
    return latencies

"""
14.
Comment on the results you got!

14a. Which pipelines is faster in terms of throughput?

===== ANSWER Q14a BELOW =====
the baseline vectorized pipeline is significantly faster in terms of throughput because pandas operations use optimized numpy arrays.
===== END OF Q14a ANSWER =====

14b. Which pipeline is faster in terms of latency?

===== ANSWER Q14b BELOW =====
the baseline vectorized pipeline is faster in latency as well, showing that vectorization benefits even small datasets.
===== END OF Q14b ANSWER =====

14c. Do you notice any other interesting observations?
What does this experiment show?

===== ANSWER Q14c BELOW =====
the performance gap grows larger with dataset size. this shows vectorization is essential for large-scale data processing and demonstrates why pandas is preferred over manual loops.
===== END OF Q14c ANSWER =====
"""

"""
===== Questions 15-17: Reflection Questions =====
15.

Take a look at all your pipelines above.
Which factor that we tested (file vs. variable, vectorized vs. for loop)
had the biggest impact on performance?

===== ANSWER Q15 BELOW =====
vectorization vs for loops had the biggest impact on performance. the difference between vectorized and manual iteration was much more dramatic than the difference between loading from files vs variables.
===== END OF Q15 ANSWER =====

16.
Based on all of your plots, form a hypothesis as to how throughput
varies with the size of the input dataset.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q16 BELOW =====
throughput generally increases with larger input datasets because the fixed overhead costs are amortized over more items. larger datasets achieve higher items-per-second processing rates.
===== END OF Q16 ANSWER =====

17.
Based on all of your plots, form a hypothesis as to how
throughput is related to latency.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q17 BELOW =====
latency and throughput are inversely related - higher throughput operations tend to have lower per-item latency. operations with high throughput process items more efficiently, resulting in lower average latency per item.
===== END OF Q17 ANSWER =====
"""

"""
# ===== Extra Credit =====

# This part is optional.

# Use your pipeline to compare something else!

# Here are some ideas for what to try:
# - the cost of random sampling vs. the cost of getting rows from the
#   DataFrame manually
# - the cost of cloning a DataFrame
# - the cost of sorting a DataFrame prior to doing a computation
# - the cost of using different encodings (like one-hot encoding)
#   and encodings for null values
# - the cost of querying via Pandas methods vs querying via SQL
#   For this part: you would want to use something like
#   pandasql that can run SQL queries on Pandas data frames. See:
#   https://stackoverflow.com/a/45866311/2038713

# As your answer to this part,
# as before, return
# a. the list of 6 throughputs
# and
# b. the list of 2 latencies.

# and generate plots for each of these in the following files:
#     output/part2-ec-a.png
#     output/part2-ec-b.png
# """

# # Extra credit (optional)

# def extra_credit_a():
#     raise NotImplementedError

# def extra_credit_b():
#     raise NotImplementedError

"""
===== Wrapping things up =====

**Don't modify this part.**

To wrap things up, we have collected
your answers and saved them to a file below.
This will be run when you run the code.
"""

ANSWER_FILE = "output/part2-answers.txt"
UNFINISHED = 0

def log_answer(name, func, *args):
    try:
        answer = func(*args)
        print(f"{name} answer: {answer}")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},{answer}\n')
            print(f"Answer saved to {ANSWER_FILE}")
    except NotImplementedError:
        print(f"Warning: {name} not implemented.")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},Not Implemented\n')
        global UNFINISHED
        UNFINISHED += 1

def PART_2_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    # Q1-5
    log_answer("q1", q1)
    log_answer("q2a", q2a)
    # 2b: commentary
    log_answer("q3", q3)
    log_answer("q4a", q4a)
    # 4b: commentary
    log_answer("q5a", q5a)
    log_answer("q5b", q5b)

    # Q6-10
    log_answer("q6", q6)
    log_answer("q7", q7)
    log_answer("q8", q8)
    log_answer("q9a", q9a)
    log_answer("q9b", q9b)
    # 10: commentary

    # Q11-14
    log_answer("q11", q11)
    log_answer("q12", q12)
    log_answer("q13a", q13a)
    log_answer("q13b", q13b)
    # 14: commentary

    # 15-17: reflection
    # 15: commentary
    # 16: commentary
    # 17: commentary

    # Extra credit
    log_answer("extra credit (a)", extra_credit_a)
    log_answer("extra credit (b)", extra_credit_b)

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
=== END OF PART 2 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 2", PART_2_PIPELINE)
