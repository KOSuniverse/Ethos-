"""
Example Usage: Corporate Sales and Inventory Analytics

This script demonstrates how to use the DataScientist tool for
real-world corporate sales and inventory analysis scenarios.
"""

from data_scientist import (
    DataScientist,
    generate_sample_sales_data,
    generate_sample_inventory_data
)
import pandas as pd


def main():
    """Run example analyses."""
    
    print("=" * 100)
    print(" " * 30 + "CORPORATE DATA ANALYTICS DASHBOARD")
    print("=" * 100)
    
    # Initialize the DataScientist tool
    ds = DataScientist()
    
    # ============================================================================
    # SCENARIO 1: Sales Performance Analysis
    # ============================================================================
    print("\n" + "=" * 100)
    print("SCENARIO 1: SALES PERFORMANCE ANALYSIS - Identifying Top Revenue Drivers")
    print("=" * 100)
    
    # Generate realistic sales data (or load from your CSV file)
    print("\nLoading sales data...")
    sales_data = generate_sample_sales_data(2000)
    print(f"✓ Loaded {len(sales_data)} sales transactions")
    print(f"✓ Date range: {sales_data['Date'].min()} to {sales_data['Date'].max()}")
    print(f"✓ Total revenue: ${sales_data['Sales'].sum():,.2f}")
    
    # Perform Pareto analysis to find which products drive 80% of revenue
    print("\nPerforming Pareto Analysis (80/20 Rule)...")
    sales_analysis = ds.analyze_sales_by_product(
        sales_data,
        product_column='Product',
        sales_column='Sales',
        save_chart='corporate_sales_pareto.png'
    )
    
    print(f"\n📊 KEY INSIGHTS:")
    print(f"   • Total unique products: {sales_analysis['total_products']}")
    print(f"   • Products driving 80% of revenue: {sales_analysis['products_contributing_80_percent']}")
    print(f"   • Efficiency ratio: {sales_analysis['percentage_of_products_for_80_sales']:.1f}% of products = 80% of revenue")
    
    print(f"\n🏆 TOP PERFORMERS (Contributing to 80% of sales):")
    top_products = sales_analysis['top_products'].head(5)
    for idx, row in top_products.iterrows():
        print(f"   {row['Category']:12} - Revenue: ${row['Value']:>12,.2f} | Cumulative: {row['Cumulative_Percentage']:>5.1f}%")
    
    print(f"\n✓ Pareto chart saved as: corporate_sales_pareto.png")
    
    # ============================================================================
    # SCENARIO 2: Multi-Dimensional Sales Analysis with Pivot Tables
    # ============================================================================
    print("\n" + "=" * 100)
    print("SCENARIO 2: REGIONAL & TEMPORAL SALES ANALYSIS - Pivot Table Deep Dive")
    print("=" * 100)
    
    # Analysis 1: Sales by Region and Quarter
    print("\n📊 PIVOT TABLE 1: Sales by Region and Quarter")
    print("-" * 100)
    regional_quarterly_pivot = ds.create_sales_pivot_analysis(
        sales_data,
        row_dimension='Region',
        column_dimension='Quarter',
        value_metric='Sales',
        aggfunc='sum'
    )
    print(regional_quarterly_pivot.round(2))
    
    # Analysis 2: Average transaction value by Product and Region
    print("\n📊 PIVOT TABLE 2: Average Transaction Value by Product and Region")
    print("-" * 100)
    avg_transaction_pivot = ds.create_pivot_table(
        sales_data,
        index='Product',
        columns='Region',
        values='Sales',
        aggfunc='mean',
        margins=True,
        margins_name='Overall Avg'
    )
    print(avg_transaction_pivot.round(2))
    
    # Analysis 3: Quantity sold by Product and Quarter
    print("\n📊 PIVOT TABLE 3: Quantity Sold by Product and Quarter")
    print("-" * 100)
    quantity_pivot = ds.create_pivot_table(
        sales_data,
        index='Product',
        columns='Quarter',
        values='Quantity',
        aggfunc='sum',
        margins=True
    )
    print(quantity_pivot)
    
    # ============================================================================
    # SCENARIO 3: Inventory Management and Optimization
    # ============================================================================
    print("\n" + "=" * 100)
    print("SCENARIO 3: INVENTORY TURNOVER ANALYSIS - Optimizing Stock Levels")
    print("=" * 100)
    
    # Generate inventory data (or load from your CSV file)
    print("\nLoading inventory data...")
    inventory_data = generate_sample_inventory_data(100)
    print(f"✓ Loaded {len(inventory_data)} inventory items")
    print(f"✓ Total stock value: ${(inventory_data['Stock_Level'] * inventory_data['Unit_Cost']).sum():,.2f}")
    
    # Perform inventory turnover Pareto analysis
    print("\nPerforming Inventory Turnover Analysis...")
    inventory_analysis = ds.analyze_inventory_turnover(
        inventory_data,
        item_column='Item',
        turnover_column='Turnover',
        save_chart='inventory_turnover_pareto.png'
    )
    
    print(f"\n📦 INVENTORY INSIGHTS:")
    print(f"   • Total SKUs: {inventory_analysis['total_items']}")
    print(f"   • Fast-moving items (80% turnover): {inventory_analysis['fast_moving_items_count']}")
    print(f"   • Stock optimization opportunity: {inventory_analysis['percentage_fast_moving']:.1f}% of items drive 80% of turnover")
    
    print(f"\n⚡ TOP FAST-MOVING ITEMS:")
    fast_movers = inventory_analysis['fast_moving_items'].head(10)
    for idx, row in fast_movers.iterrows():
        print(f"   {row['Category']:15} | Turnover: {row['Value']:>10,.0f} | Cumulative: {row['Cumulative_Percentage']:>5.1f}%")
    
    print(f"\n✓ Inventory Pareto chart saved as: inventory_turnover_pareto.png")
    
    # Create inventory pivot analysis by category
    print("\n📊 PIVOT TABLE 4: Inventory Metrics by Category")
    print("-" * 100)
    inventory_category_pivot = ds.create_pivot_table(
        inventory_data,
        index='Category',
        values=['Turnover', 'Stock_Level', 'Unit_Cost'],
        aggfunc={
            'Turnover': 'sum',
            'Stock_Level': 'mean',
            'Unit_Cost': 'mean'
        },
        margins=True,
        margins_name='Overall'
    )
    print(inventory_category_pivot.round(2))
    
    # ============================================================================
    # SCENARIO 4: Custom Analysis - Loading Your Own Data
    # ============================================================================
    print("\n" + "=" * 100)
    print("SCENARIO 4: LOADING YOUR OWN DATA")
    print("=" * 100)
    
    print("""
To analyze your own data, you can:

1. Load from CSV file:
   ds.load_data('your_sales_data.csv')

2. Load from DataFrame:
   df = pd.read_excel('your_data.xlsx')
   ds.load_data(df)

3. Load from dictionary:
   data = {'Product': [...], 'Sales': [...], 'Region': [...]}
   ds.load_data(data)

Then use the same analysis methods shown above!
    """)
    
    # ============================================================================
    # Summary and Recommendations
    # ============================================================================
    print("\n" + "=" * 100)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 100)
    
    print(f"""
Based on the analysis:

1. SALES OPTIMIZATION:
   • Focus on top {sales_analysis['products_contributing_80_percent']} products for maximum ROI
   • Consider promotional strategies for underperforming products
   • Regional variations suggest targeted marketing opportunities

2. INVENTORY MANAGEMENT:
   • Prioritize {inventory_analysis['fast_moving_items_count']} fast-moving items for stock availability
   • Review slow-moving items for potential clearance or reduced ordering
   • Optimize warehouse space allocation based on turnover rates

3. DATA-DRIVEN DECISIONS:
   • Use Pareto charts to identify key drivers in any business metric
   • Leverage pivot tables for multi-dimensional trend analysis
   • Regular analysis helps maintain competitive advantage

4. NEXT STEPS:
   • Import your actual sales/inventory data
   • Customize analysis parameters for your business needs
   • Schedule regular reporting cycles for ongoing insights
    """)
    
    print("=" * 100)
    print(" " * 35 + "Analysis Complete!")
    print("=" * 100)
    print("\nGenerated files:")
    print("  • corporate_sales_pareto.png")
    print("  • inventory_turnover_pareto.png")
    print("\n")


if __name__ == "__main__":
    main()
