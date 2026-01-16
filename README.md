# Ethos - Data Science Analytics Tool

A powerful Python-based data science tool designed to help analyze sales and inventory data at a corporate level. This tool provides essential analytics capabilities including Pareto chart generation and pivot table creation for data mining.

## Features

### 🔍 Pareto Chart Analysis
- **80/20 Rule Visualization**: Identify the vital few items that drive the majority of your results
- **Sales Analysis**: Discover which products contribute to 80% of revenue
- **Inventory Optimization**: Identify fast-moving vs. slow-moving inventory items
- **Visual Charts**: Generate professional Pareto charts with cumulative percentage lines

### 📊 Pivot Table Creation
- **Multi-Dimensional Analysis**: Aggregate data across multiple dimensions
- **Flexible Aggregation**: Support for sum, mean, count, and other aggregation functions
- **Sales by Region/Quarter**: Analyze sales patterns across time and geography
- **Inventory Metrics**: Aggregate inventory data by category, location, or other dimensions
- **Grand Totals**: Automatic calculation of row and column totals

## Installation

1. Clone this repository:
```bash
git clone https://github.com/KOSuniverse/Ethos-.git
cd Ethos-
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Running the Example

```bash
python data_scientist.py
```

This will:
- Generate sample sales and inventory data
- Perform Pareto analysis on both datasets
- Create pivot tables for multi-dimensional analysis
- Save Pareto charts as PNG files

### Basic Usage

```python
from data_scientist import DataScientist, generate_sample_sales_data

# Initialize the tool
ds = DataScientist()

# Load your data (CSV, DataFrame, or dictionary)
sales_data = generate_sample_sales_data(1000)
ds.load_data(sales_data)

# Create a Pareto chart
pareto_df, fig = ds.create_pareto_chart(
    category_column='Product',
    value_column='Sales',
    title='Sales Pareto Analysis',
    save_path='sales_pareto.png'
)

# Create a pivot table
pivot = ds.create_pivot_table(
    index='Region',
    columns='Quarter',
    values='Sales',
    aggfunc='sum',
    margins=True
)
print(pivot)
```

## Use Cases

### 1. Sales Analysis
Identify which products drive the majority of revenue:
```python
sales_analysis = ds.analyze_sales_by_product(
    sales_data,
    product_column='Product',
    sales_column='Sales'
)
print(f"Top {sales_analysis['products_contributing_80_percent']} products drive 80% of sales")
```

### 2. Inventory Management
Find fast-moving items that require frequent restocking:
```python
inventory_analysis = ds.analyze_inventory_turnover(
    inventory_data,
    item_column='Item',
    turnover_column='Turnover'
)
print(f"Fast-moving items: {inventory_analysis['fast_moving_items_count']}")
```

### 3. Regional Performance
Compare sales across regions and time periods:
```python
regional_pivot = ds.create_sales_pivot_analysis(
    sales_data,
    row_dimension='Region',
    column_dimension='Quarter',
    value_metric='Sales'
)
```

### 4. Custom Pivot Tables
Create custom aggregations for specific business needs:
```python
custom_pivot = ds.create_pivot_table(
    data=sales_data,
    index=['Region', 'Product'],
    columns='Quarter',
    values='Sales',
    aggfunc='mean',
    margins=True
)
```

## API Reference

### DataScientist Class

#### Methods

- **`load_data(data)`**: Load data from DataFrame, CSV file, or dictionary
- **`create_pareto_chart(...)`**: Generate a Pareto chart for 80/20 analysis
- **`create_pivot_table(...)`**: Create a pivot table for data aggregation
- **`analyze_sales_by_product(...)`**: Analyze sales data with Pareto principle
- **`analyze_inventory_turnover(...)`**: Analyze inventory turnover rates
- **`create_sales_pivot_analysis(...)`**: Create sales-specific pivot analysis

### Utility Functions

- **`generate_sample_sales_data(n_records)`**: Generate sample sales data for testing
- **`generate_sample_inventory_data(n_items)`**: Generate sample inventory data for testing

## Data Format Requirements

### Sales Data
Your sales data should include:
- Product/Item identifier column
- Sales value or quantity column
- Optional: Region, Time period, Category columns for pivot analysis

Example:
```csv
Product,Region,Quarter,Sales,Quantity,Date
Product_A,North,Q1,1250.50,45,2023-01-15
Product_B,South,Q1,980.25,32,2023-01-16
```

### Inventory Data
Your inventory data should include:
- Item identifier column
- Turnover or movement metric column
- Optional: Category, Location, Stock level columns

Example:
```csv
Item,Category,Turnover,Stock_Level,Unit_Cost
Item_001,Electronics,5420,150,45.99
Item_002,Clothing,3210,200,19.99
```

## Dependencies

- pandas >= 2.0.0
- matplotlib >= 3.7.0
- numpy >= 1.24.0

## Output

The tool generates:
1. **Pareto Charts**: PNG images showing bar charts with cumulative percentage lines
2. **Data Frames**: Formatted tables with analysis results
3. **Insights**: Statistical summaries identifying key contributors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Data Science Analytics Tool for Corporate Sales and Inventory Analysis