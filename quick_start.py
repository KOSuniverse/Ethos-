"""
Quick Start Guide - Data Science Analytics Tool

This guide shows you how to get started with the Ethos Data Science tool
in under 5 minutes.
"""

from data_scientist import DataScientist, generate_sample_sales_data, generate_sample_inventory_data

def quick_start_guide():
    """Quick start demo - 5 minutes to insights!"""
    
    print("\n" + "="*80)
    print("QUICK START GUIDE - 5 Minutes to Data Science Insights")
    print("="*80 + "\n")
    
    # Step 1: Create the tool
    print("Step 1: Initialize the Data Science Tool")
    print("-" * 80)
    ds = DataScientist()
    print("✓ DataScientist tool initialized\n")
    
    # Step 2: Load your data
    print("Step 2: Load Your Data")
    print("-" * 80)
    print("For this demo, we'll use sample data.")
    print("In practice, you would load your own CSV file:\n")
    print("   ds.load_data('your_sales_data.csv')\n")
    
    sales_data = generate_sample_sales_data(500)
    print(f"✓ Loaded {len(sales_data)} sales records\n")
    
    # Step 3: Create a Pareto Chart
    print("Step 3: Create a Pareto Chart (80/20 Analysis)")
    print("-" * 80)
    print("Find which products drive 80% of your revenue:\n")
    
    pareto_result, fig = ds.create_pareto_chart(
        sales_data,
        category_column='Product',
        value_column='Sales',
        title='Sales by Product - Pareto Analysis',
        save_path='quick_start_pareto.png',
        show_plot=False
    )
    
    top_80 = pareto_result[pareto_result['Cumulative_Percentage'] <= 80]
    
    print(f"✓ Chart saved as 'quick_start_pareto.png'")
    print(f"✓ {len(top_80)} out of {len(pareto_result)} products drive 80% of sales")
    print(f"\nTop performers:")
    for idx, row in top_80.head(3).iterrows():
        print(f"   • {row['Category']}: ${row['Value']:,.2f} ({row['Cumulative_Percentage']:.1f}% cumulative)")
    
    # Step 4: Create a Pivot Table
    print("\n\nStep 4: Create a Pivot Table")
    print("-" * 80)
    print("Analyze sales across multiple dimensions:\n")
    
    pivot = ds.create_pivot_table(
        sales_data,
        index='Region',
        columns='Quarter',
        values='Sales',
        aggfunc='sum',
        margins=True,
        margins_name='Total'
    )
    
    print("Sales by Region and Quarter:")
    print(pivot.round(2))
    
    # Step 5: Done!
    print("\n\n" + "="*80)
    print("CONGRATULATIONS! You've completed the quick start guide.")
    print("="*80)
    print("\nWhat you learned:")
    print("  ✓ How to initialize the DataScientist tool")
    print("  ✓ How to load data (CSV, DataFrame, or dict)")
    print("  ✓ How to create Pareto charts for 80/20 analysis")
    print("  ✓ How to create pivot tables for multi-dimensional analysis")
    print("\nNext steps:")
    print("  1. Try with your own sales or inventory data")
    print("  2. Explore advanced features in example_usage.py")
    print("  3. Read the full documentation in README.md")
    print("\nHappy analyzing! 📊\n")


if __name__ == "__main__":
    quick_start_guide()
