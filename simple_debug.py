#!/usr/bin/env python3
"""
Simple debug to show exactly what each app calculates and displays
"""

import pandas as pd
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Employee class from both versions
from app import Employee as NewEmployee
from app_old import Employee as OldEmployee

def simple_debug():
    """Simple debug for ארי"""
    
    # File path
    excel_file = "פעילות חודשית (35).xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ File {excel_file} not found!")
        return
    
    print(f"🔍 Simple Debug for ארי")
    print("=" * 50)
    
    # Read and process data exactly like both apps do
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
    print()
    
    # Show the raw data
    print("📋 Raw data for ארי:")
    for i, row in ari_data.iterrows():
        print(f"Row {i}: Date={row['date']}, Dog={row['dog name']}, Payment={row['payment to service recipients']}, Travel={row['travel']}")
    print()
    
    # Create both Employee objects
    new_emp = NewEmployee('ארי', df)
    old_emp = OldEmployee('ארי', df)
    
    print("🔍 DETAILED COMPARISON:")
    print("=" * 50)
    print(f"Walking numbers:     New={new_emp.walking_numbers}, Old={old_emp.walking_numbers}")
    print(f"Days worked:         New={new_emp.days_worked}, Old={old_emp.days_worked}")
    print(f"Travel days:         New={new_emp.travel_days}, Old={old_emp.travel_days}")
    print(f"Additional charge:   New={new_emp.additional_charge}, Old={old_emp.additional_charge}")
    print(f"Yami mismeret:       New={new_emp.yami_mismeret}, Old={old_emp.yami_mismeret}")
    print(f"Tutor:               New={new_emp.tutor}, Old={old_emp.tutor}")
    print(f"Has monthly free:    New={new_emp.has_monthly_free}, Old={old_emp.has_monthly_free}")
    print(f"Payment:             New={new_emp.payment}, Old={old_emp.payment}")
    print()
    
    # Show what each app would display
    print("📱 WHAT EACH APP DISPLAYS:")
    print("=" * 50)
    print("NEW APP:")
    print(f"  Walking numbers: {new_emp.walking_numbers}")
    print(f"  Number of days worked: {new_emp.days_worked}")
    print(f"  Number of travel days: {new_emp.travel_days}")
    print()
    print("OLD APP:")
    print(f"  Walking numbers: {old_emp.walking_numbers}")
    print(f"  Number of days worked: {old_emp.days_worked}")
    print(f"  Number of travel days: {old_emp.travel_days}")
    print()
    
    # Check if there are any differences in the calculation methods
    print("🔍 CALCULATION METHOD COMPARISON:")
    print("=" * 50)
    
    # Walking numbers calculation
    new_walking = len(ari_data['dog name'].dropna())
    old_walking = len(ari_data['dog name'].dropna())
    print(f"Walking numbers calculation: New={new_walking}, Old={old_walking}")
    
    # Days worked calculation
    new_days = ari_data['date'].nunique()
    old_days = ari_data['date'].nunique()
    print(f"Days worked calculation: New={new_days}, Old={old_days}")
    
    # Travel days calculation
    new_travel_data = ari_data.copy()
    new_travel_data.travel = new_travel_data.travel.astype(str)
    new_travel_data = new_travel_data[~new_travel_data.travel.str.contains('לא')]
    new_travel_days = len(new_travel_data['date'].unique())
    
    old_travel_data = ari_data.copy()
    old_travel_data.travel = old_travel_data.travel.astype(str)
    old_travel_data = old_travel_data[~old_travel_data.travel.str.contains('לא')]
    old_travel_days = len(old_travel_data['date'].unique())
    
    print(f"Travel days calculation: New={new_travel_days}, Old={old_travel_days}")

if __name__ == "__main__":
    simple_debug()
