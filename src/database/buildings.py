from src.database.db_connection import get_db_connection

# # Function to query building upgrade details
# def get_building_info(building_name, level):
#     conn = get_db_connection()
#     c = conn.cursor()

#     # Get the building tier from buildings table
#     c.execute("SELECT tier FROM buildings WHERE building_name = ?", (building_name,))
#     building = c.fetchone()

#     if not building:
#         return f"Building '{building_name}' not found."

#     tier = building[0]

#     # Query the respective tier table
#     query = f"SELECT upgrade_cost, cumulative_cost, value FROM {tier}_tier WHERE level = ?"
#     c.execute(query, (level,))
#     result = c.fetchone()

#     if not result:
#         conn.close()
#         return f"Level '{level}' not found for building '{building_name}' in tier '{tier}'."

#     upgrade_cost, cumulative_cost, value = result

#     conn.close()

#     return {
#         'tier': tier,
#         'upgrade_cost': upgrade_cost,
#         'cumulative_cost': cumulative_cost,
#         'value': value
#     }

def get_buildings(page = 1):
    conn = get_db_connection()
    c = conn.cursor()

    # Calculate the offset for the query based on page number
    buildings_per_page = 10
    offset = (page - 1) * buildings_per_page

    c.execute("SELECT * FROM buildings LIMIT ? OFFSET ?", (buildings_per_page, offset))
    buildings = c.fetchall()
    if not buildings:
        return f"No buildings"
    
    buildingsList = []

    for building in buildings:
        name, tier, maxLevel, setName = building

        buildingDict = {
            "Building Name": name,
            "Tier": tier,
            "Max Level": maxLevel
        }

        if setName != "" and setName is not None:
            buildingDict["Set"] = setName

        buildingsList.append(buildingDict)
    
    return buildingsList

# Function to calculate the maximum number of pages
def get_max_pages():
    conn = get_db_connection()
    c = conn.cursor()

    # Get the total number of buildings
    c.execute("SELECT COUNT(*) FROM buildings")
    total_buildings = c.fetchone()[0]

    # Calculate the number of pages needed (10 buildings per page)
    buildings_per_page = 10
    max_pages = (total_buildings + buildings_per_page - 1) // buildings_per_page

    return max_pages