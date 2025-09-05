#!/usr/bin/env python3
"""
Test what the app is actually calculating
"""

import pandas as pd
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Employee class
from app import Employee

def test_app_calculation():
    """Test what the app calculates for ארי"""
    
    # File path
    excel_file = "פעילות חודשית (35).xlsx"
    
    print(f"🔍 Testing App Calculation for ארי")
    print("=" * 50)
    
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
    print(f"📊 Total rows for ארי: {len(ari_data)}")
    
    # Create Employee object
    emp = Employee('ארי', df)
    
    print(f"📊 Employee object calculations:")
    print(f"  Walking numbers: {emp.walking_numbers}")
    print(f"  Days worked: {emp.days_worked}")
    print(f"  Travel days: {emp.travel_days}")
    print(f"  Additional charge: {emp.additional_charge}")
    print(f"  Yami mismeret: {emp.yami_mismeret}")
    print(f"  Tutor: {emp.tutor}")
    print(f"  Payment: {emp.payment}")
    print()
    
    # Check if the issue is in the calculation method
    print("🔍 Checking calculation method:")
    dog_names = ari_data['dog name'].dropna()
    print(f"  Dog names found: {list(dog_names)}")
    print(f"  Count of dog names: {len(dog_names)}")
    print(f"  Method result: {emp.calculate_walking_numbers()}")
    print()
    
    # Check if there's a different issue
    print("🔍 Checking if there's a different issue:")
    print(f"  Total rows: {len(ari_data)}")
    print(f"  Rows with dog names: {len(ari_data[ari_data['dog name'].notna()])}")
    print(f"  Rows with additional activity: {len(ari_data[ari_data['additional activity'].notna()])}")
    print(f"  Rows with any data: {len(ari_data[(ari_data['dog name'].notna()) | (ari_data['additional activity'].notna())])}")
    
    # If the app shows 5, maybe it's counting total rows or something else
    if emp.walking_numbers == 2:
        print("✅ The calculation is correct (2), but the app might be showing something else")
        print("   The app might be displaying total rows (5) instead of walking numbers (2)")
    else:
        print("❌ There's a bug in the calculation method")

if __name__ == "__main__":
    test_app_calculation()
