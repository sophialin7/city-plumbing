import csv
import os

FILES = {
    'SJ_INFRA': 'storm_manholes.csv',
    'SF_INFRA': 'stormwater.csv',
    'SJ_ZONING': 'Zoning_Districts.csv',
    'STATE_ZONING': 'California_Statewide_Zoning_North_2662355680020073874.csv'
}

def main():
    nodes = []
    edges = []
    
    # Process Cities
    nodes.append({'ID:ID': 'CITY_SJ', 'Name': 'San Jose', ':LABEL': 'City'})
    nodes.append({'ID:ID': 'CITY_SF', 'Name': 'San Francisco', ':LABEL': 'City'})

    # --- 1. San Jose Infrastructure & Zoning
    if os.path.exists(FILES['SJ_INFRA']):
        with open(FILES['SJ_INFRA'], mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                id_ = "SJ_MH_{row['FACILITYID']}"
                nodes.append({'ID:ID': id_, 'Name': "SJ Manhole {row['FACILITYID']}", ':LABEL': 'Infrastructure;Manhole', 'City': 'San Jose', 'Year': row.get('INSTALLYEAR')})
                edges.append({':START_ID': id_, ':END_ID': 'CITY_SJ', ':TYPE': 'IN_CITY'})

    if os.path.exists(FILES['SJ_ZONING']):
        with open(FILES['SJ_ZONING'], mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                z_id = "ZONING_SJ_{row['ZONING']}"
                nodes.append({'ID:ID': z_id, 'Name': f"Zone {row['ZONING']}", ':LABEL': 'ZoningDistrict', 'Code': row['ZONINGABBREV']})
                edges.append({':START_ID': z_id, ':END_ID': 'CITY_SJ', ':TYPE': 'ZONING_OF'})

    # 2. San Francisco Infrastructure
    if os.path.exists(FILES['SF_INFRA']):
        with open(FILES['SF_INFRA'], mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                id_ = "SF_IN_{row['DPW_Node_ID']}"
                nodes.append({'ID:ID': id_, 'Name': f"SF Inlet {row['DPW_Node_ID']}", ':LABEL': 'Infrastructure;Inlet', 'City': 'San Francisco'})
                edges.append({':START_ID': id_, ':END_ID': 'CITY_SF', ':TYPE': 'IN_CITY'})
                nb = row.get('analysis_neighborhood')
                if nb:
                    nb_id = f"NB_{nb.replace(' ', '_')}"
                    edges.append({':START_ID': id_, ':END_ID': nb_id, ':TYPE': 'LOCATED_IN'})

    # 3. Statewide Zoning (Requirements Layer) 
    if os.path.exists(FILES['STATE_ZONING']):
        with open(FILES['STATE_ZONING'], mode='r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                req_name = row.get('ucd_description')
                if req_name:
                    req_id = "REQ_{req_name.replace(' ', '_')}"
                    nodes.append({'ID:ID': req_id, 'Name': req_name, ':LABEL': 'Requirement', 'Class': row.get('New_Class')})

    # Exporting
    with open('master_nodes.csv', 'w', newline='', encoding='utf-8') as f:
        # determine headers from all node dictionaries
        keys = set().union(*(d.keys() for d in nodes))
        writer = csv.DictWriter(f, fieldnames=sorted(list(keys)))
        writer.writeheader()
        writer.writerows(nodes)

    with open('master_edges.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[':START_ID', ':END_ID', ':TYPE'])
        writer.writeheader()
        writer.writerows(edges)

    print("CSVs generated: master_nodes.csv and master_edges.csv")

if __name__ == "__main__":
    main()
