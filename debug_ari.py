#!/usr/bin/env python3
"""
Debug script to compare calculations between old and new app versions
for dog walker "ארי" using the "פעילות חודשית" file
"""

import pandas as pd
import sys
import os

# Add the current directory to path so we can import from both app files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Employee class from both versions
from app import Employee as NewEmployee
from app_old import Employee as OldEmployee

def debug_ari_calculations():
    """Debug calculations for dog walker 'ארי'"""
    
    # File path
    excel_file = "פעילות חודשית (35).xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ File {excel_file} not found!")
        return
    
    print(f"🔍 Debugging calculations for dog walker 'ארי' using file: {excel_file}")
    print("=" * 80)
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        print(f"📊 Excel file loaded successfully. Shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        print()
        
        # Normalize columns (same as in new app)
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
        
        print("🔄 Data after normalization:")
        print(f"📋 Normalized columns: {list(df.columns)}")
        print()
        
        # Check if 'ארי' exists in the data
        if 'name' not in df.columns:
            print("❌ No 'name' column found after normalization!")
            return
            
        unique_names = df['name'].dropna().unique()
        print(f"👥 All unique names in data: {list(unique_names)}")
        
        # Look for 'ארי' (exact match and similar)
        ari_variants = [name for name in unique_names if 'ארי' in str(name)]
        print(f"🔍 Names containing 'ארי': {ari_variants}")
        
        if not ari_variants:
            print("❌ No dog walker named 'ארי' found!")
            return
            
        # Use the first match
        ari_name = ari_variants[0]
        print(f"✅ Using name: '{ari_name}'")
        print()
        
        # Filter data for ארי
        ari_data = df[df['name'] == ari_name]
        print(f"📊 Data for '{ari_name}': {len(ari_data)} rows")
        print()
        
        # Show raw data for ארי
        print("📋 Raw data for ארי:")
        print(ari_data[['date', 'dog name', 'payment to service recipients', 'travel', 'shift compensation']].to_string())
        print()
        
        # Calculate walking days using different methods
        print("🚶 Walking Days Calculations:")
        print("-" * 40)
        
        # Method 1: Simple count of non-null dog names
        walking_numbers_simple = len(ari_data['dog name'].dropna())
        print(f"1. Simple dog name count: {walking_numbers_simple}")
        
        # Method 2: Count unique dates with dog names
        numeric_df = ari_data[ari_data['dog name'].notna() & ari_data['dog name'].ne('')]
        numeric_df = numeric_df[numeric_df['payment to service recipients'].apply(lambda x: str(x).isnumeric() and not pd.isna(x))]
        walking_days_unique = len(numeric_df['date'].unique())
        print(f"2. Unique dates with numeric payments: {walking_days_unique}")
        
        # Method 3: Count unique dates with any dog name
        walking_days_any = ari_data[ari_data['dog name'].notna() & ari_data['dog name'].ne('')]['date'].nunique()
        print(f"3. Unique dates with any dog name: {walking_days_any}")
        
        # Method 4: Count unique dates (total)
        total_days = ari_data['date'].nunique()
        print(f"4. Total unique dates: {total_days}")
        
        print()
        
        # Create Employee objects from both versions
        print("👨‍💼 Creating Employee objects from both versions:")
        print("-" * 50)
        
        # New version
        try:
            new_employee = NewEmployee(ari_name, df)
            print("✅ New version Employee created successfully")
            print(f"   Walking numbers: {new_employee.walking_numbers}")
            print(f"   Days worked: {new_employee.days_worked}")
            print(f"   Travel days: {new_employee.travel_days}")
            print(f"   Payment: {new_employee.payment}")
        except Exception as e:
            print(f"❌ Error creating new version Employee: {e}")
            new_employee = None
        
        # Old version
        try:
            old_employee = OldEmployee(ari_name, df)
            print("✅ Old version Employee created successfully")
            print(f"   Walking numbers: {old_employee.walking_numbers}")
            print(f"   Days worked: {old_employee.days_worked}")
            print(f"   Travel days: {old_employee.travel_days}")
            print(f"   Payment: {old_employee.payment}")
        except Exception as e:
            print(f"❌ Error creating old version Employee: {e}")
            old_employee = None
        
        print()
        
        # Compare results
        if new_employee and old_employee:
            print("🔍 COMPARISON RESULTS:")
            print("=" * 50)
            print(f"Walking numbers - New: {new_employee.walking_numbers}, Old: {old_employee.walking_numbers}")
            print(f"Days worked - New: {new_employee.days_worked}, Old: {old_employee.days_worked}")
            print(f"Travel days - New: {new_employee.travel_days}, Old: {old_employee.travel_days}")
            print(f"Payment - New: {new_employee.payment}, Old: {old_employee.payment}")
            
            if new_employee.walking_numbers != old_employee.walking_numbers:
                print("⚠️  DIFFERENCE FOUND in walking numbers!")
            else:
                print("✅ Walking numbers are the same")
        
        print()
        print("🔍 Detailed analysis of walking numbers calculation:")
        print("-" * 60)
        
        # Show the exact data used in walking numbers calculation
        dog_names = ari_data['dog name'].dropna()
        print(f"Dog names (non-null): {list(dog_names)}")
        print(f"Count of dog names: {len(dog_names)}")
        
        # Show payment data
        payments = ari_data['payment to service recipients'].dropna()
        print(f"Payment values: {list(payments)}")
        print(f"Count of payments: {len(payments)}")
        
        # Show travel data
        travel = ari_data['travel'].dropna()
        print(f"Travel values: {list(travel)}")
        print(f"Count of travel entries: {len(travel)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ari_calculations()
