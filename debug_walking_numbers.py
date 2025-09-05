#!/usr/bin/env python3
"""
Debug the walking numbers calculation specifically
"""

import pandas as pd
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Employee class
from app import Employee

def debug_walking_numbers():
    """Debug walking numbers calculation"""
    
    # File path
    excel_file = "פעילות חודשית (35).xlsx"
    
    print(f"🔍 Debug Walking Numbers Calculation for ארי")
    print("=" * 60)
    
    # Read and process data exactly like the app does
    df = pd.read_excel(excel_file)
    columns = {
        'תאריך': 'Date', 'שם': 'Name', 'מתלמד': 'Apprentice', 
        'תגמול משמרות': 'Shift compensation', 'שם הכלב': 'Dog name', 
        'מחיר ללקוח': 'Price to customer', 'תשלום למ.ש': 'Payment to service recipients',
        'הצמדה': 'Link', 'פעילות נוספת': 'Additional activity', 
        'חונך': 'Tutor', 'הערות': 'Comments', 'תשלום נוסף': 'Additional charge', 
        'נסיעות': 'Travel'
    }
    df.rename(columns=columns, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%y')
    df.columns = map(str.lower, df.columns)
    
    # Filter for ארי
    ari_data = df[df['name'] == 'ארי']
    print(f"📊 ארי data shape: {ari_data.shape}")
    print()
    
    # Show the dog name column specifically
    print("🐕 Dog name column for ארי:")
    print("-" * 40)
    for i, (idx, row) in enumerate(ari_data.iterrows()):
        dog_name = row['dog name']
        print(f"Row {i+1}: '{dog_name}' (type: {type(dog_name)}, isna: {pd.isna(dog_name)})")
    print()
    
    # Test the calculation step by step
    print("🔍 Step-by-step calculation:")
    print("-" * 40)
    
    # Step 1: Get the dog name column
    dog_names_column = ari_data['dog name']
    print(f"1. Dog names column: {list(dog_names_column)}")
    
    # Step 2: Drop NaN values
    dog_names_dropped = dog_names_column.dropna()
    print(f"2. After dropna(): {list(dog_names_dropped)}")
    
    # Step 3: Get length
    length = len(dog_names_dropped)
    print(f"3. Length: {length}")
    print()
    
    # Test the method directly
    print("🔍 Testing the method directly:")
    print("-" * 40)
    
    # Create Employee object
    emp = Employee('ארי', df)
    
    # Test the method
    method_result = emp.calculate_walking_numbers()
    print(f"Method result: {method_result}")
    
    # Test the attribute
    print(f"Attribute value: {emp.walking_numbers}")
    
    # Check if they match
    if method_result == emp.walking_numbers:
        print("✅ Method and attribute match")
    else:
        print("❌ Method and attribute don't match!")
    
    # Check if the result is correct
    expected = 2  # Should be 2 based on our analysis
    if method_result == expected:
        print(f"✅ Result is correct: {method_result}")
    else:
        print(f"❌ Result is wrong: {method_result}, expected: {expected}")
        
        # Let's see what might be causing this
        print("\n🔍 Investigating the discrepancy:")
        print(f"Total rows: {len(ari_data)}")
        print(f"Rows with dog names: {len(ari_data[ari_data['dog name'].notna()])}")
        print(f"Rows with additional activity: {len(ari_data[ari_data['additional activity'].notna()])}")
        
        # Maybe the method is counting something else?
        print(f"\nAll non-null values in dog name column: {ari_data['dog name'].notna().sum()}")
        print(f"All non-null values in additional activity column: {ari_data['additional activity'].notna().sum()}")

if __name__ == "__main__":
    debug_walking_numbers()
