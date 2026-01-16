"""
Data Science Analytics Tool for Corporate Sales and Inventory Analysis

This module provides tools to analyze sales and inventory data at a corporate level:
- Pareto Chart generation for 80/20 analysis
- Pivot Table creation for multi-dimensional data aggregation
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional, Union


class DataScientist:
    """
    A data science tool for analyzing sales and inventory data.
    
    Features:
    - Pareto chart generation for identifying key drivers (80/20 rule)
    - Pivot table creation for data aggregation and analysis
    - Support for sales and inventory data mining
    """
    
    def __init__(self):
        """Initialize the DataScientist tool."""
        self.data = None
        
    def load_data(self, data: Union[pd.DataFrame, str, Dict]) -> pd.DataFrame:
        """
        Load data from various sources.
        
        Args:
            data: Can be a DataFrame, file path (CSV), or dictionary
            
        Returns:
            pd.DataFrame: Loaded data
        """
        if isinstance(data, pd.DataFrame):
            self.data = data
        elif isinstance(data, str):
            # Assume it's a file path
            self.data = pd.read_csv(data)
        elif isinstance(data, dict):
            self.data = pd.DataFrame(data)
        else:
            raise ValueError("Data must be a DataFrame, file path, or dictionary")
            
        return self.data
    
    def create_pareto_chart(
        self,
        data: Optional[pd.DataFrame] = None,
        category_column: str = None,
        value_column: str = None,
        title: str = "Pareto Chart",
        save_path: Optional[str] = None,
        show_plot: bool = True
    ) -> tuple:
        """
        Create a Pareto chart to identify the vital few from the trivial many.
        
        The Pareto principle (80/20 rule) helps identify which categories
        contribute the most to the total value.
        
        Args:
            data: DataFrame to analyze (uses self.data if None)
            category_column: Column name for categories
            value_column: Column name for values to analyze
            title: Chart title
            save_path: Optional path to save the chart
            show_plot: Whether to display the plot
            
        Returns:
            tuple: (DataFrame with Pareto analysis, matplotlib figure)
        """
        if data is None:
            data = self.data
            
        if data is None:
            raise ValueError("No data available. Please load data first.")
            
        if category_column is None or value_column is None:
            raise ValueError("Both category_column and value_column must be specified")
        
        # Aggregate data by category
        pareto_data = data.groupby(category_column)[value_column].sum().sort_values(ascending=False)
        
        # Calculate cumulative percentage
        cumulative_sum = pareto_data.cumsum()
        cumulative_percentage = (cumulative_sum / pareto_data.sum()) * 100
        
        # Create the plot
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Bar chart for values
        x_pos = np.arange(len(pareto_data))
        ax1.bar(x_pos, pareto_data.values, color='steelblue', alpha=0.7)
        ax1.set_xlabel('Categories', fontsize=12)
        ax1.set_ylabel(f'{value_column}', fontsize=12, color='steelblue')
        ax1.tick_params(axis='y', labelcolor='steelblue')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(pareto_data.index, rotation=45, ha='right')
        
        # Line chart for cumulative percentage
        ax2 = ax1.twinx()
        ax2.plot(x_pos, cumulative_percentage.values, color='red', marker='o', linewidth=2)
        ax2.set_ylabel('Cumulative Percentage (%)', fontsize=12, color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.axhline(y=80, color='green', linestyle='--', linewidth=1, label='80% threshold')
        ax2.set_ylim([0, 105])
        ax2.legend(loc='lower right')
        
        # Title and grid
        plt.title(title, fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        if show_plot:
            plt.show()
        
        # Create result DataFrame
        result_df = pd.DataFrame({
            'Category': pareto_data.index,
            'Value': pareto_data.values,
            'Cumulative_Value': cumulative_sum.values,
            'Cumulative_Percentage': cumulative_percentage.values
        })
        
        return result_df, fig
    
    def create_pivot_table(
        self,
        data: Optional[pd.DataFrame] = None,
        index: Union[str, List[str]] = None,
        columns: Optional[Union[str, List[str]]] = None,
        values: Optional[Union[str, List[str]]] = None,
        aggfunc: Union[str, Dict] = 'sum',
        fill_value: Optional[float] = None,
        margins: bool = False,
        margins_name: str = 'Total'
    ) -> pd.DataFrame:
        """
        Create a pivot table for multi-dimensional data analysis.
        
        Args:
            data: DataFrame to analyze (uses self.data if None)
            index: Column(s) to use as row index
            columns: Column(s) to use as column headers
            values: Column(s) to aggregate
            aggfunc: Aggregation function ('sum', 'mean', 'count', etc.)
            fill_value: Value to replace NaN
            margins: Add row/column totals
            margins_name: Name for the totals row/column
            
        Returns:
            pd.DataFrame: Pivot table
        """
        if data is None:
            data = self.data
            
        if data is None:
            raise ValueError("No data available. Please load data first.")
            
        if index is None:
            raise ValueError("Index must be specified")
        
        pivot = pd.pivot_table(
            data,
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            fill_value=fill_value,
            margins=margins,
            margins_name=margins_name
        )
        
        return pivot
    
    def analyze_sales_by_product(
        self,
        sales_data: pd.DataFrame,
        product_column: str = 'Product',
        sales_column: str = 'Sales',
        save_chart: Optional[str] = None
    ) -> Dict:
        """
        Analyze sales data to identify top-performing products using Pareto analysis.
        
        Args:
            sales_data: Sales data DataFrame
            product_column: Column name for products
            sales_column: Column name for sales values
            save_chart: Optional path to save the Pareto chart
            
        Returns:
            dict: Analysis results including Pareto data and insights
        """
        self.load_data(sales_data)
        
        # Create Pareto chart
        pareto_df, fig = self.create_pareto_chart(
            category_column=product_column,
            value_column=sales_column,
            title=f"Sales Pareto Analysis by {product_column}",
            save_path=save_chart,
            show_plot=False
        )
        
        # Identify products contributing to 80% of sales
        products_80_percent = pareto_df[pareto_df['Cumulative_Percentage'] <= 80]
        
        analysis = {
            'pareto_data': pareto_df,
            'total_products': len(pareto_df),
            'products_contributing_80_percent': len(products_80_percent),
            'top_products': products_80_percent,
            'percentage_of_products_for_80_sales': 
                (len(products_80_percent) / len(pareto_df)) * 100,
            'figure': fig
        }
        
        return analysis
    
    def analyze_inventory_turnover(
        self,
        inventory_data: pd.DataFrame,
        item_column: str = 'Item',
        turnover_column: str = 'Turnover',
        save_chart: Optional[str] = None
    ) -> Dict:
        """
        Analyze inventory turnover to identify slow-moving and fast-moving items.
        
        Args:
            inventory_data: Inventory data DataFrame
            item_column: Column name for inventory items
            turnover_column: Column name for turnover rate
            save_chart: Optional path to save the Pareto chart
            
        Returns:
            dict: Analysis results including Pareto data and insights
        """
        self.load_data(inventory_data)
        
        # Create Pareto chart
        pareto_df, fig = self.create_pareto_chart(
            category_column=item_column,
            value_column=turnover_column,
            title=f"Inventory Turnover Pareto Analysis",
            save_path=save_chart,
            show_plot=False
        )
        
        # Identify fast-moving items (contributing to 80% of turnover)
        fast_moving = pareto_df[pareto_df['Cumulative_Percentage'] <= 80]
        
        analysis = {
            'pareto_data': pareto_df,
            'total_items': len(pareto_df),
            'fast_moving_items_count': len(fast_moving),
            'fast_moving_items': fast_moving,
            'percentage_fast_moving': (len(fast_moving) / len(pareto_df)) * 100,
            'figure': fig
        }
        
        return analysis
    
    def create_sales_pivot_analysis(
        self,
        sales_data: pd.DataFrame,
        row_dimension: str,
        column_dimension: Optional[str] = None,
        value_metric: str = 'Sales',
        aggfunc: str = 'sum'
    ) -> pd.DataFrame:
        """
        Create a pivot table for sales analysis across multiple dimensions.
        
        Args:
            sales_data: Sales data DataFrame
            row_dimension: Dimension for rows (e.g., 'Region', 'Product')
            column_dimension: Dimension for columns (e.g., 'Quarter', 'Year')
            value_metric: Metric to aggregate (e.g., 'Sales', 'Quantity')
            aggfunc: Aggregation function ('sum', 'mean', 'count')
            
        Returns:
            pd.DataFrame: Pivot table with sales analysis
        """
        self.load_data(sales_data)
        
        pivot = self.create_pivot_table(
            index=row_dimension,
            columns=column_dimension,
            values=value_metric,
            aggfunc=aggfunc,
            margins=True,
            margins_name='Grand Total'
        )
        
        return pivot


def generate_sample_sales_data(n_records: int = 1000) -> pd.DataFrame:
    """
    Generate sample sales data for testing.
    
    Args:
        n_records: Number of records to generate
        
    Returns:
        pd.DataFrame: Sample sales data
    """
    np.random.seed(42)
    
    products = ['Product_A', 'Product_B', 'Product_C', 'Product_D', 'Product_E',
                'Product_F', 'Product_G', 'Product_H', 'Product_I', 'Product_J']
    regions = ['North', 'South', 'East', 'West']
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    
    # Create Pareto distribution (20% of products drive 80% of sales)
    product_weights = [0.25, 0.20, 0.15, 0.10, 0.08, 0.07, 0.05, 0.04, 0.03, 0.03]
    
    data = {
        'Product': np.random.choice(products, n_records, p=product_weights),
        'Region': np.random.choice(regions, n_records),
        'Quarter': np.random.choice(quarters, n_records),
        'Sales': np.random.exponential(1000, n_records) + 100,
        'Quantity': np.random.randint(1, 100, n_records),
        'Date': pd.date_range('2023-01-01', periods=n_records, freq='D')[:n_records]
    }
    
    return pd.DataFrame(data)


def generate_sample_inventory_data(n_items: int = 50) -> pd.DataFrame:
    """
    Generate sample inventory data for testing.
    
    Args:
        n_items: Number of inventory items to generate
        
    Returns:
        pd.DataFrame: Sample inventory data
    """
    np.random.seed(42)
    
    # Create items with varying turnover rates (Pareto distribution)
    items = [f'Item_{i:03d}' for i in range(1, n_items + 1)]
    categories = ['Electronics', 'Clothing', 'Food', 'Furniture', 'Books']
    
    # Simulate turnover with Pareto distribution
    turnover = np.random.pareto(2, n_items) * 1000 + 50
    
    data = {
        'Item': items,
        'Category': np.random.choice(categories, n_items),
        'Turnover': turnover,
        'Stock_Level': np.random.randint(10, 500, n_items),
        'Reorder_Point': np.random.randint(5, 100, n_items),
        'Unit_Cost': np.random.uniform(5, 500, n_items)
    }
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Example usage
    print("=" * 80)
    print("Data Science Analytics Tool - Example Usage")
    print("=" * 80)
    
    # Initialize the data scientist tool
    ds = DataScientist()
    
    # Generate sample sales data
    print("\n1. Generating sample sales data...")
    sales_data = generate_sample_sales_data(1000)
    print(f"   Generated {len(sales_data)} sales records")
    print("\n   Sample data:")
    print(sales_data.head())
    
    # Pareto analysis for sales
    print("\n2. Performing Pareto Analysis on Sales by Product...")
    sales_analysis = ds.analyze_sales_by_product(
        sales_data,
        save_chart='sales_pareto.png'
    )
    print(f"   Total products: {sales_analysis['total_products']}")
    print(f"   Products contributing to 80% of sales: {sales_analysis['products_contributing_80_percent']}")
    print(f"   Percentage: {sales_analysis['percentage_of_products_for_80_sales']:.1f}%")
    print("\n   Top contributing products:")
    print(sales_analysis['top_products'])
    
    # Create pivot table for sales analysis
    print("\n3. Creating Pivot Table: Sales by Region and Quarter...")
    sales_pivot = ds.create_sales_pivot_analysis(
        sales_data,
        row_dimension='Region',
        column_dimension='Quarter',
        value_metric='Sales'
    )
    print(sales_pivot)
    
    # Generate sample inventory data
    print("\n4. Generating sample inventory data...")
    inventory_data = generate_sample_inventory_data(50)
    print(f"   Generated {len(inventory_data)} inventory items")
    print("\n   Sample data:")
    print(inventory_data.head())
    
    # Pareto analysis for inventory
    print("\n5. Performing Pareto Analysis on Inventory Turnover...")
    inventory_analysis = ds.analyze_inventory_turnover(
        inventory_data,
        save_chart='inventory_pareto.png'
    )
    print(f"   Total items: {inventory_analysis['total_items']}")
    print(f"   Fast-moving items (80% turnover): {inventory_analysis['fast_moving_items_count']}")
    print(f"   Percentage: {inventory_analysis['percentage_fast_moving']:.1f}%")
    print("\n   Fast-moving items:")
    print(inventory_analysis['fast_moving_items'])
    
    # Create pivot table for inventory analysis
    print("\n6. Creating Pivot Table: Inventory by Category...")
    inventory_pivot = ds.create_pivot_table(
        inventory_data,
        index='Category',
        values=['Turnover', 'Stock_Level'],
        aggfunc={'Turnover': 'sum', 'Stock_Level': 'mean'},
        margins=True
    )
    print(inventory_pivot)
    
    print("\n" + "=" * 80)
    print("Analysis complete! Charts saved as 'sales_pareto.png' and 'inventory_pareto.png'")
    print("=" * 80)
