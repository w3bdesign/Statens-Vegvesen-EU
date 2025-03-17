import pandas as pd
import sqlite3
from pathlib import Path

def create_database():
    """Create SQLite database and tables"""
    conn = sqlite3.connect('eu_kontroll.db')
    c = conn.cursor()
    
    # Create vehicles table
    c.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,
            make TEXT,
            model TEXT,
            year INTEGER,
            vehicle_type TEXT,
            fuel_type TEXT
        )
    ''')
    
    # Create inspections table
    c.execute('''
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY,
            vehicle_id INTEGER,
            inspection_date TEXT,
            approved BOOLEAN,
            mileage INTEGER,
            num_1er_faults INTEGER,
            num_2er_faults INTEGER,
            num_3er_faults INTEGER,
            num_4er_faults INTEGER,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
        )
    ''')
    
    conn.commit()
    return conn

def process_csv(csv_path):
    """Process the CSV file and insert data into SQLite database"""
    # Read CSV with appropriate encoding for Norwegian characters
    df = pd.read_csv(csv_path, encoding='latin1')
    
    # Create database and get connection
    conn = create_database()
    c = conn.cursor()
    
    # Process each row
    for _, row in df.iterrows():
        # Insert vehicle data
        c.execute('''
            INSERT OR IGNORE INTO vehicles (make, model, year, vehicle_type, fuel_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            row['Kjøretøymerke'],
            row['Kjøretøy Modell'],
            int(row['Første gang registrert']),
            row['Kjøretøy Gruppekode'],
            row['Drivstofftype']
        ))
        
        # Get vehicle_id
        vehicle_id = c.lastrowid if c.lastrowid else c.execute(
            'SELECT id FROM vehicles WHERE make=? AND model=? AND year=?',
            (row['Kjøretøymerke'], row['Kjøretøy Modell'], int(row['Første gang registrert']))
        ).fetchone()[0]
        
        # Insert inspection data
        c.execute('''
            INSERT INTO inspections (
                vehicle_id, inspection_date, approved, mileage,
                num_1er_faults, num_2er_faults, num_3er_faults, num_4er_faults
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vehicle_id,
            f"{row['PKK Kontrollmåned']}",
            row['Godkjent'] == 'Ja',
            int(row['Kilometerstand']),
            int(row['Ant 1er merknad']),
            int(row['Ant 2er merknad']),
            int(row['Ant 3er merknad']),
            int(row['Ant 4er merknad'])
        ))
    
    # Create views for common queries
    c.execute('''
        CREATE VIEW IF NOT EXISTS vehicle_stats AS
        SELECT 
            v.make,
            v.model,
            v.year,
            COUNT(*) as total_inspections,
            SUM(CASE WHEN i.approved THEN 1 ELSE 0 END) as approved_count,
            ROUND(AVG(CASE WHEN i.approved THEN 1.0 ELSE 0.0 END) * 100, 2) as approval_rate,
            AVG(i.num_2er_faults + i.num_3er_faults) as avg_serious_faults
        FROM vehicles v
        JOIN inspections i ON v.id = i.vehicle_id
        GROUP BY v.make, v.model, v.year
        HAVING total_inspections >= 30
    ''')
    
    conn.commit()
    conn.close()

def main():
    # Process Q1 2023 data
    csv_path = Path('../data/PKK-2023-kvartal1/PKK-2023-kvartal1.csv')
    if not csv_path.exists():
        print(f"Error: Could not find CSV file at {csv_path}")
        return
    
    process_csv(csv_path)
    print("Data processing complete. Database created successfully.")

if __name__ == "__main__":
    main()
