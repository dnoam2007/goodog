import streamlit as st
import pandas as pd

# Default settings (can be overridden from the sidebar controls)
shift_compensation = 15
single_bus_ticket_price = 12.5
monthly_free_threshold_days = 15
monthly_free_amount = 225

st.set_page_config(page_title="Goodog • Payroll & Clients", page_icon="🐕", layout="wide")


class Employee:
    def __init__(self, name, df):
        self.name = name
        self.df = df[df['name'] == name]
        self.days_worked = self.calculate_days_worked()
        self.travel_days = self.calculate_travel_days()
        self.walking_numbers = self.calculate_walking_numbers()
        self.additional_charge= pd.to_numeric(self.df['additional charge'].dropna(), errors='coerce').sum()
        self.additional_activity = self.calculate_additional_activity()
        self.yami_mismeret = self.calculate_yami_mismeret()
        self.anan=False
        self.payment, self.pirot = self.calculate_payment()

        self.has_monthly_free = self.has_monthly_free()
        self.tutor= self.calculate_tutor()
        self.JSON = self.json()

    def calculate_walking_numbers(self):
        # Remove both NaN values and 'nan' strings
        dog_names = self.df['dog name'].dropna()
        dog_names = dog_names[dog_names != 'nan']  # Remove 'nan' strings
        return len(dog_names)

    def calculate_yami_mismeret(self):
        # remove nan

        return len(self.df['shift compensation'].dropna().tolist())

    def calculate_tutor(self):
        # remove nan
        return len(self.df['tutor'].dropna().tolist())

    def calculate_days_worked(self):
        # count unique dates
        return self.df['date'].nunique()

    def calculate_travel_days(self):

        data_temp = self.df.copy()
        # Make 'travel' column string type
        data_temp.travel = data_temp.travel.astype(str)

        data_temp = data_temp[~data_temp.travel.str.contains('לא')]
        # Compute unique dates
        dates = data_temp['date'].unique()
        #return len(dates)
        # remove duplicates

        dog_namesunique = self.df['dog name'].unique()
        #   return self.df['payment to service recipients'].count()
        return len(dates)

    def has_monthly_free(self):
        # By default use number of travel days, configurable threshold
        return self.travel_days >= monthly_free_threshold_days

    def calculate_payment(self):
        payment = 0
        amount=0
        #remove values that are "ענ"ן"
        df=self.df
        #remove the values that are aaa
        df =df[df['payment to service recipients'].apply(lambda x: 'ענ"ן' not in str(x))]
        x=df['payment to service recipients'].dropna().astype(int).sum()
        pirot=df['payment to service recipients'].dropna().astype(int).value_counts()
        #cheak if pirot is empty
        if pirot.empty:
            self.anan=True
        #count how many כן we have in shift compensation
        y=len(df['shift compensation'].dropna().tolist())*shift_compensation
       # z=sum(df['additional charge'].dropna().astype(int))
        z = self.additional_charge

        payment=x+y+z

        if self.has_monthly_free():
            payment += monthly_free_amount
        else:
            payment += self.travel_days * single_bus_ticket_price
        return payment,pirot

    def calculate_additional_activity(self):
        # count how many values we have from each kind in the additional activity column
        return self.df['additional activity'].value_counts()

    def calculate_walking_days(self):
        # count non nan values in the Payment to service recipients column
        list = self.df['payment to service recipients']
        count = 0
        # remove the rows where 'dog name' is empty
        numeric_df = self.df[self.df['dog name'].notna() & self.df['dog name'].ne('')]
        numeric_df = numeric_df[
            numeric_df['payment to service recipients'].apply(lambda x: x.isnumeric() and not pd.isna(x))]
        dates = numeric_df['date'].unique()
        # remove duplicates

        #   return self.df['payment to service recipients'].count()
        return len(dates)


    def json(self):
        return {
            'name': self.name,
            'days_worked': self.days_worked,
            'Anan':self.anan,
            'payment': self.payment,
            'pirot': self.pirot,
            'travel_days': self.travel_days,
            'has_monthly_free': self.has_monthly_free,
            'additional_charge': self.additional_charge,
            'tutor': self.tutor,
            'additional_activity': self.additional_activity,
            'yami_mismeret': self.yami_mismeret,
            'walking_numbers': self.walking_numbers
        }

    def __str__(self):
        output = f'Employee {self.name} Information:\n'
        output += f'Number of days worked: {self.days_worked}\n'
        output += f'Number of travel days: {self.travel_days}\n'
        output += f'Walking numbers: {self.walking_numbers}\n'
        output += f'Additional charge: {self.additional_charge}\n'
        output += f'Additional activity: {self.additional_activity}\n'
        output += f'Has monthly free: {self.has_monthly_free}\n'
        if self.anan:
            output += 'Anan: true\n'
        else:
            output += 'Anan: false\n'
        output += f'Payment: {self.payment}\n'
        if not self.pirot.empty:
            output += 'Pirot: \n'
            for key, value in self.pirot.items():
                output += f"\t לשלם: {key}, כמות: {value}\n"
        else:
            output += 'There are no pirot values.\n'
        output += f'Tutor: {self.tutor}\n'
        output += f'Yami mismeret: {self.yami_mismeret}\n'
        return output

    def display_employee(self):
        # Compact and readable CSS styling
        st.markdown("""
            <style>
            .employee-card {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 8px;
                margin: 8px 0;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                color: #212529;
            }
            .employee-header {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 24px;
                font-weight: 800;
                margin-bottom: 8px;
                text-align: center;
                color: #495057;
                border-bottom: 1px solid #dee2e6;
                padding-bottom: 4px;
            }
            .info-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr 1fr;
                gap: 6px;
                margin: 8px 0;
            }
            .info-item {
                background: #ffffff;
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #dee2e6;
                text-align: center;
            }
            .info-label {
                font-size: 16px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.3px;
                color: #6c757d;
                margin-bottom: 2px;
            }
            .info-value {
                font-size: 20px;
                font-weight: 800;
                color: #212529;
            }
            .section-title {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 16px;
                font-weight: 700;
                margin: 8px 0 4px 0;
                color: #495057;
                border-bottom: 1px solid #dee2e6;
                padding-bottom: 2px;
            }
            .activities-container {
                background: #ffffff;
                padding: 6px;
                border-radius: 6px;
                margin: 6px 0;
                border: 1px solid #dee2e6;
            }
            .activity-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 3px 0;
                border-bottom: 1px solid #f8f9fa;
            }
            .activity-item:last-child {
                border-bottom: none;
            }
            .activity-name {
                font-size: 16px;
                font-weight: 600;
                color: #495057;
            }
            .activity-count {
                background: #28a745;
                color: white;
                padding: 1px 6px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 700;
            }
            .payment-card {
                background: linear-gradient(135deg, #28a745, #20c997);
                padding: 8px;
                border-radius: 6px;
                text-align: center;
                margin: 8px 0;
                box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
            }
            .payment-amount {
                font-size: 28px;
                font-weight: 900;
                color: white;
                margin: 2px 0;
            }
            .payment-label {
                font-size: 15px;
                font-weight: 700;
                color: white;
                opacity: 0.9;
            }
            .status-badges {
                display: flex;
                gap: 4px;
                margin: 6px 0;
                flex-wrap: wrap;
            }
            .status-badge {
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 10px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }
            .badge-yes {
                background: #28a745;
                color: white;
            }
            .badge-no {
                background: #dc3545;
                color: white;
            }
            .pirot-section {
                background: #ffffff;
                padding: 6px;
                border-radius: 6px;
                margin: 6px 0;
                border: 1px solid #dee2e6;
            }
            .employee-divider {
                background: linear-gradient(to right, transparent, #6c757d, transparent);
                height: 1px;
                margin: 10px 0;
            }
            </style>
        """, unsafe_allow_html=True)

        # Start employee card
        st.markdown("<div class='employee-card'>", unsafe_allow_html=True)

        # Header with employee name
        st.markdown(f"<div class='employee-header'>👤 {self.name}</div>", unsafe_allow_html=True)

        # Key metrics in a compact grid layout - reordered as requested
        st.markdown("<div class='info-grid'>", unsafe_allow_html=True)
        
        # Walking numbers
        st.markdown(f"""
            <div class='info-item'>
                <div class='info-label'>🐕 Walking Numbers</div>
                <div class='info-value'>{self.walking_numbers}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Yami mismeret
        st.markdown(f"""
            <div class='info-item'>
                <div class='info-label'>🌙 Yami Mismeret</div>
                <div class='info-value'>{self.yami_mismeret}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Travel days
        st.markdown(f"""
            <div class='info-item'>
                <div class='info-label'>🚗 Travel Days</div>
                <div class='info-value'>{self.travel_days}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Days without travel (days worked - travel days) - after travel days
        days_without_travel = self.days_worked - self.travel_days
        st.markdown(f"""
            <div class='info-item'>
                <div class='info-label'>🏠 Days Without Travel</div>
                <div class='info-value'>{days_without_travel}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Additional charge
        st.markdown(f"""
            <div class='info-item'>
                <div class='info-label'>➕ Additional Charge</div>
                <div class='info-value'>₪{self.additional_charge}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Monthly free status
        st.markdown(f"""
            <div class='info-item'>
                <div class='info-label'>💳 Monthly Free</div>
                <div class='info-value'>{'Yes' if self.has_monthly_free else 'No'}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Days worked - after monthly free
        st.markdown(f"""
            <div class='info-item'>
                <div class='info-label'>📅 Days Worked</div>
                <div class='info-value'>{self.days_worked}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Anan status
        st.markdown(f"""
            <div class='info-item'>
                <div class='info-label'>👤 Anan</div>
                <div class='info-value'>{'Yes' if self.anan else 'No'}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

        # Additional Activities Section
        has_additional_activity = not self.additional_activity.empty or self.tutor > 0
        st.markdown("<div class='section-title'>🎯 Additional Activities</div>", unsafe_allow_html=True)
        
        if has_additional_activity:
            st.markdown("<div class='activities-container'>", unsafe_allow_html=True)
            # Display regular additional activities
            if not self.additional_activity.empty:
                for activity, count in self.additional_activity.items():
                    st.markdown(f"""
                        <div class='activity-item'>
                            <span class='activity-name'>{activity}</span>
                            <span class='activity-count'>{count} times</span>
                        </div>
                    """, unsafe_allow_html=True)

            # Display tutor activities
            if self.tutor > 0:
                st.markdown(f"""
                    <div class='activity-item'>
                        <span class='activity-name'>Tutor</span>
                        <span class='activity-count'>{self.tutor}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='activities-container'>No additional activities</div>", unsafe_allow_html=True)

        # Payment display
        st.markdown(f"""
            <div class='payment-card'>
                <div class='payment-label'>Total Payment for {self.name}</div>
                <div class='payment-amount'>₪{self.payment:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

        # Pirot Information
        st.markdown("<div class='section-title'>📊 Pirot Information</div>", unsafe_allow_html=True)
        st.markdown("<div class='pirot-section'>", unsafe_allow_html=True)
        if not self.pirot.empty:
            st.write(self.pirot.to_frame())
        else:
            st.markdown("<div style='text-align: center; opacity: 0.7;'>No pirot values available</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # End employee card
        st.markdown("</div>", unsafe_allow_html=True)

        # Add gradient divider after each employee
        st.markdown("<div class='employee-divider'></div>", unsafe_allow_html=True)


class Client:
    def __init__(self, dog_name, df):
        self.dog_name = dog_name
        self.df = df[df['dog name'] == dog_name]
        self.payment, self.pirot, self.total_walks, self.paid_walks = self.calculate_payment()
        # Add number of walks calculation
        self.walking_dates = self.df['date'].nunique()
        self.walkers = self.df['name'].unique().tolist()

    def calculate_payment(self):
        df = self.df
        # Exclude rows marked as cloud (ענ"ן)
        df = df[df['price to customer'].apply(lambda x: 'ענ"ן' not in str(x))]
        # Coerce to numeric for robust comparisons
        price_series = pd.to_numeric(df['price to customer'].dropna(), errors='coerce')
        payment = int(price_series.dropna().sum())
        pirot = price_series.dropna().astype(int).value_counts()
        total_walks = len(df)
        paid_walks = int((price_series > 0).sum())
        return payment, pirot, total_walks, paid_walks

    def display_client(self):
        # Custom CSS for client display
        st.markdown("""
            <style>
            .client-name {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                color: #2c2f50;
                padding: 10px;
                margin-bottom: 20px;
                border-bottom: 3px solid #3498db;
            }
            .walks-info {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }
            .payment-info {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                color: white;
            }
            .pirot-item {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 20px;
                margin: 10px 0;
                padding: 8px;
                background-color: white;
                border-radius: 4px;
            }
            .client-divider {
                background: linear-gradient(to right, #f0f2f6, #3498db, #f0f2f6);
                height: 3px;
                margin: 30px 0;
                border-radius: 2px;
            }
            </style>
        """, unsafe_allow_html=True)

        # Start client container
        #st.markdown("<div class='client-container'>", unsafe_allow_html=True)

        # Dog Name (Large)
        st.markdown(f"<div class='client-name'>🐕 {self.dog_name}</div>", unsafe_allow_html=True)

        # Walks Information (Large) — show only paid walks
        st.markdown(f"""
            <div class='walks-info'>
                הולכות בתשלום: {self.paid_walks}
            </div>
        """, unsafe_allow_html=True)

        # Payment Information (Large with color)
        payment_color = "red" if self.payment >= 1000 else "orange" if self.payment >= 500 else "green"
        st.markdown(f"""
            <div class='payment-info' style='background-color: {payment_color};'>
                Total Payment: ₪{self.payment}
            </div>
        """, unsafe_allow_html=True)

        # Pirot Information (Large)
        if not self.pirot.empty:
            st.markdown("<div class='pirot-container'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; margin-bottom: 15px;'>Payment Breakdown:</h3>",
                        unsafe_allow_html=True)
            for price, count in self.pirot.items():
                st.markdown(f"""
                    <div class='pirot-item'>
                        Price: ₪{price} | Number of Walks: {count}
                    </div>
                """, unsafe_allow_html=True)
            # Add total walks line (including unpaid)
            st.markdown(f"""
                <div class='pirot-item'>
                    Total Walks: {self.total_walks}
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Dog Walkers List
        if self.walkers:
            st.markdown("<div class='walker-list'>", unsafe_allow_html=True)
            st.markdown("<h4>Dog Walkers:</h4>", unsafe_allow_html=True)
            for walker in self.walkers:
                st.markdown(f"• {walker}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # End client container
        st.markdown("</div>", unsafe_allow_html=True)

        # Add divider
        st.markdown("<div class='client-divider'></div>", unsafe_allow_html=True)

    def json(self):
        return {
            'dog_name': self.dog_name,
            'payment': self.payment,
            'pirot': self.pirot,
            'total_walks': self.total_walks,
            'walking_dates': self.walking_dates,
            'walkers': self.walkers
        }

    def __str__(self):
        output = f'Client {self.dog_name} Information:\n'
        output += f'Payment: {self.payment}\n'
        output += f'Pirot: {self.pirot}\n'
        output += f'Total Walks: {self.total_walks}\n'
        output += f'Walking Dates: {self.walking_dates}\n'
        return output
def calculate_employee_payments_for_debug1(excel_file):
    # load the excel file
    df = pd.read_excel(excel_file)
    columns = {'תאריך': 'Date', 'שם': 'Name', 'מתלמד': 'Apprentice', 'תגמול משמרת': 'Shift compensation',
               'שם הכלב': 'Dog name', 'מחיר ללקוח': 'Price to customer',
               'תשלום למ.ש': 'Payment to service recipients',
               'הצמדה': 'Link', 'פעילות נוספת': 'Additional activity', 'חונך': 'Tutor', 'הערות': 'Comments',
               'תשלום נוסף': 'Additional charge', 'נסיעות': 'Travel'}
    df.rename(columns=columns, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%y')

    #do it on the coulm name
    df.columns = map(str.lower, df.columns)
    # derive employees list safely
    employees = df['name'].dropna().unique() if 'name' in df.columns else []
    shift_compensatio=10
    for employee in employees:
        e = Employee(employee, df)
        print(e)
        print('-------------------------')
def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize and translate Hebrew/English columns to expected canonical names."""
    col_map = {
        'תאריך': 'Date',
        'שם': 'Name',
        'מתלמד': 'Apprentice',
        'תגמול משמרת': 'Shift compensation',
        'שם הכלב': 'Dog name',
        'מחיר ללקוח': 'Price to customer',
        'תשלום למ.ש': 'Payment to service recipients',
        'הצמדה': 'Link',
        'פעילות נוספת': 'Additional activity',
        'חונך': 'Tutor',
        'הערות': 'Comments',
        'תשלום נוסף': 'Additional charge',
        'נסיעות': 'Travel',
        # fallback English variations
        'date': 'Date',
        'name': 'Name',
        'apprentice': 'Apprentice',
        'shift compensation': 'Shift compensation',
        'dog name': 'Dog name',
        'price to customer': 'Price to customer',
        'payment to service recipients': 'Payment to service recipients',
        'link': 'Link',
        'additional activity': 'Additional activity',
        'tutor': 'Tutor',
        'comments': 'Comments',
        'additional charge': 'Additional charge',
        'travel': 'Travel',
    }

    # strip and lowercase incoming columns for matching
    sanitized_cols = {c: str(c).strip() for c in df.columns}
    df = df.rename(columns=sanitized_cols)
    lower_map = {c: c.lower() for c in df.columns}
    df = df.rename(columns=lower_map)
    # apply mapping to canonical form
    df = df.rename(columns=lambda c: col_map.get(c, col_map.get(c.lower(), c)))
    return df


def _read_excel(uploaded_file) -> pd.DataFrame:
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    df = _normalize_columns(df)
    # Coerce Date column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'].astype(str).str.strip(), format='%d.%m.%y', errors='coerce')
    # Standardize to lowercase for downstream code
    df.columns = map(str.lower, df.columns)
    # Clean key string columns if present
    for col in ['name', 'dog name', 'travel']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


def calculate_payments():
    st.title("Goodog — Payroll and Clients Dashboard 🐕")
    with st.sidebar:
        st.header("Settings")
        st.markdown("---")
        uploaded_file = st.file_uploader("Upload Excel (.xlsx)", type='xlsx')
        st.markdown("---")
        st.markdown("**App Version: 2.3.1**")

        # Configurable parameters
        global shift_compensation, single_bus_ticket_price, monthly_free_threshold_days, monthly_free_amount
        shift_compensation = st.number_input("Shift compensation (₪)", min_value=0, max_value=1000, value=int(shift_compensation))
        single_bus_ticket_price = st.number_input("Single bus ticket (₪)", min_value=0.0, max_value=100.0, value=float(single_bus_ticket_price))
        monthly_free_threshold_days = st.number_input("Monthly pass threshold (travel days)", min_value=0, max_value=31, value=int(monthly_free_threshold_days))
        monthly_free_amount = st.number_input("Monthly pass amount (₪)", min_value=0, max_value=5000, value=int(monthly_free_amount))

        view = st.radio("View", options=["Dog walkers", "Clients"], index=0, horizontal=False)

    if uploaded_file is None:
        st.info("Upload an Excel file to begin.")
        return
    try:
        df = _read_excel(uploaded_file)
    except Exception as exc:
        st.error(f"Failed to read Excel: {exc}")
        return

    if view == "Dog walkers":
        if 'name' not in df.columns:
            st.error("The file is missing a 'name' column after normalization.")
            return
        employees = sorted([e for e in df['name'].dropna().unique() if str(e).strip()])
        all_option = "Select All"
        selection = st.multiselect("Select dog walkers", [all_option] + employees, default=[all_option])
        if all_option in selection:
            selection = employees

        # Summary table and per-employee display
        rows = []
        for employee_name in selection:
            try:
                e = Employee(employee_name, df)
                rows.append({
                    'name': e.name,
                    'walking_numbers': e.walking_numbers,
                    'yami_mismeret': e.yami_mismeret,
                    'travel_days': e.travel_days,
                    'days_worked': e.days_worked,
                    'additional_charge': e.additional_charge,
                    'has_monthly_free': e.has_monthly_free,
                    'payment': e.payment,
                })
            except Exception as err:
                st.warning(f"Error in {employee_name}: {err}")

        if rows:
            summary_df = pd.DataFrame(rows)
            st.subheader("Summary")
            st.dataframe(summary_df, use_container_width=True)

            csv = summary_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download summary (CSV)", csv, file_name="employees_summary.csv", mime="text/csv")

            st.subheader("Details")
            for employee_name in selection:
                try:
                    e = Employee(employee_name, df)
                    e.display_employee()
                except Exception as err:
                    st.warning(f"Error rendering {employee_name}: {err}")

    else:  # Clients
        if 'dog name' not in df.columns:
            st.error("The file is missing a 'dog name' column after normalization.")
            return

        clients = sorted([c for c in df['dog name'].dropna().unique() if isinstance(c, str) and c.strip()])
        all_option = "Select All"
        selection = st.multiselect("Select clients", [all_option] + clients, default=[all_option])
        if all_option in selection:
            selection = clients

        rows = []
        for client_name in selection:
            try:
                c = Client(client_name, df)
                rows.append({
                    'dog_name': c.dog_name,
                    'total_walks': c.total_walks,
                    'walking_dates': c.walking_dates,
                    'payment': c.payment,
                })
            except Exception as err:
                st.warning(f"Error in {client_name}: {err}")

        if rows:
            summary_df = pd.DataFrame(rows)
            st.subheader("Summary")
            st.dataframe(summary_df, use_container_width=True)
            csv = summary_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download summary (CSV)", csv, file_name="clients_summary.csv", mime="text/csv")

            st.subheader("Details")
            for client_name in selection:
                try:
                    c = Client(client_name, df)
                    c.display_client()
                except Exception as err:
                    st.warning(f"Error rendering {client_name}: {err}")

def calculate_employee_payments_for_debug(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        columns = {'תאריך': 'Date', 'שם': 'Name', 'מתלמד': 'Apprentice', 'תגמול משמרת': 'Shift compensation',
                   'שם הכלב': 'Dog name', 'מחיר ללקוח': 'Price to customer',
                   'תשלום למ.ש': 'Payment to service recipients',
                   'הצמדה': 'Link', 'פעילות נוספת': 'Additional activity', 'חונך': 'Tutor', 'הערות': 'Comments',
                   'תשלום נוסף': 'Additional charge', 'נסיעות': 'Travel'}
        df.rename(columns=columns, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%y')
        st.write(df)
        df.columns = map(str.lower, df.columns)
        #cheakbox for clients or dog walkers
        if st.checkbox('Dog walkers'):

            df['name'] = df['name'].str.strip()
            employees = df['name'].unique()
            #make multiselect box for the dog walkers add option to show all
            all_option = "Select All"
            employees_with_all = [all_option] + list(employees)  # assuming employees is your list of options
            #st.write(employees_with_all)
            selected_dog_walkers = st.multiselect('select dog walkers', employees_with_all, default=(all_option))

            if all_option in selected_dog_walkers:
                selected_dog_walkers = employees  # if 'Select All' is selected, select all employees
            for employee in selected_dog_walkers:
                e = Employee(employee, df)
                st.json(e.json())
                #st.write(e)
                st.write('-------------------------')
        # elif st.checkbox('Clients'):
        #     df['dog name'] = df['dog name'].str.strip()
        #     clients = df['dog name'].unique()
        #     for client in clients:
        #         e = Client(client, df)
        #         st.json(e.json())
        #         #st.write(e)
        #         st.write('-------------------------')
calculate_payments()
####for debug copt and run the main 28.1.24###