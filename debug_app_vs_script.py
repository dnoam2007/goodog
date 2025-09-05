#!/usr/bin/env python3
"""
Debug script to compare what the app shows vs what our script calculates
"""

import pandas as pd
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Employee class
from app import Employee

def debug_app_vs_script():
    """Debug the difference between app display and script calculation"""
    
    # File path
    excel_file = "פעילות חודשית (35).xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ File {excel_file} not found!")
        return
    
    print(f"🔍 Debug App vs Script for ארי")
    print("=" * 60)
    
    # Read and process data exactly like the app does
    df = pd.read_excel(excel_file)
    print(f"📊 Original Excel shape: {df.shape}")
    print(f"📋 Original columns: {list(df.columns)}")
    print()
    
    # Apply the same normalization as the app
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
    
    print(f"📊 After normalization shape: {df.shape}")
    print(f"📋 Normalized columns: {list(df.columns)}")
    print()
    
    # Filter for ארי
    ari_data = df[df['name'] == 'ארי']
    print(f"📊 ארי data shape: {ari_data.shape}")
    print()
    
    # Show all data for ארי
    print("📋 ALL DATA FOR ארי:")
    print("-" * 40)
    for i, (idx, row) in enumerate(ari_data.iterrows()):
        print(f"Row {i+1} (index {idx}):")
        print(f"  Date: {row['date']}")
        print(f"  Dog name: {row['dog name']}")
        print(f"  Payment: {row['payment to service recipients']}")
        print(f"  Additional activity: {row['additional activity']}")
        print(f"  Travel: {row['travel']}")
        print(f"  Shift compensation: {row['shift compensation']}")
        print()
    
    # Create Employee object
    emp = Employee('ארי', df)
    
    print("🔍 EMPLOYEE OBJECT CALCULATIONS:")
    print("=" * 50)
    print(f"Walking numbers: {emp.walking_numbers}")
    print(f"Days worked: {emp.days_worked}")
    print(f"Travel days: {emp.travel_days}")
    print(f"Additional charge: {emp.additional_charge}")
    print(f"Yami mismeret: {emp.yami_mismeret}")
    print(f"Tutor: {emp.tutor}")
    print(f"Payment: {emp.payment}")
    print()
    
    # Manual calculation to verify
    print("🔍 MANUAL CALCULATION VERIFICATION:")
    print("=" * 50)
    
    # Walking numbers - should be count of non-null dog names
    dog_names = ari_data['dog name'].dropna()
    manual_walking = len(dog_names)
    print(f"Manual walking numbers: {manual_walking}")
    print(f"Dog names found: {list(dog_names)}")
    print()
    
    # Days worked - should be count of unique dates
    manual_days = ari_data['date'].nunique()
    print(f"Manual days worked: {manual_days}")
    print(f"Unique dates: {sorted(ari_data['date'].unique())}")
    print()
    
    # Travel days
    travel_data = ari_data.copy()
    travel_data.travel = travel_data.travel.astype(str)
    travel_data = travel_data[~travel_data.travel.str.contains('לא')]
    manual_travel = len(travel_data['date'].unique())
    print(f"Manual travel days: {manual_travel}")
    print()
    
    # Additional activity
    additional_activity = ari_data['additional activity'].value_counts()
    print(f"Manual additional activity: {dict(additional_activity)}")
    print()
    
    # Check if there's a discrepancy
    if emp.walking_numbers != manual_walking:
        print("⚠️  DISCREPANCY FOUND!")
        print(f"Employee object says: {emp.walking_numbers}")
        print(f"Manual calculation says: {manual_walking}")
    else:
        print("✅ Walking numbers match between Employee object and manual calculation")

if __name__ == "__main__":
    debug_app_vs_script()
