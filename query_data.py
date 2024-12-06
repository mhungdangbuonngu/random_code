import psycopg2

def build_sql_query_individual(table, requirements, general_requirements, schema="travel_database"):
    conditions = []
    joins = ""
    
    # Define the ID column based on the table
    id_column = "id"
    if table == "hotel":
        id_column = "hotel_id"
    elif table == "restaurant":
        id_column = "res_id"
    elif table == "touristattraction":
        id_column = "attraction_id"
    
    # Handle Price_range for each table with join and conditions
    if general_requirements.get("Price_range"):
        price_range = general_requirements["Price_range"]
        if table == "hotel":
            joins += f" JOIN {schema}.hotelprice ON {schema}.hotel.hotel_id = {schema}.hotelprice.hotel_id"
            if price_range == "low":
                conditions.append(f"{schema}.hotelprice.price < 500000")
            elif price_range == "medium":
                conditions.append(f"{schema}.hotelprice.price <= 2000000")
            elif price_range == "high":
                conditions.append(f"{schema}.hotelprice.price > 2000000")
        elif table == "restaurant":
            if price_range == "low":
                conditions.append(f"CAST({schema}.restaurant.price_range->>'max_price' AS INTEGER) < 200000")
            elif price_range == "medium":
                conditions.append(f"CAST({schema}.restaurant.price_range->>'max_price' AS INTEGER) <= 600000")
            elif price_range == "high":
                conditions.append(f"CAST({schema}.restaurant.price_range->>'min_price' AS INTEGER) >= 0")
        elif table == "touristattraction":
            joins += f" JOIN {schema}.attractionprice ON {schema}.touristattraction.attraction_id = {schema}.attractionprice.attraction_id"
            if price_range == "low":
                conditions.append(f"{schema}.attractionprice.price < 500000")
            elif price_range == "medium":
                conditions.append(f"{schema}.attractionprice.price < 1500000")
            elif price_range == "high":
                conditions.append(f"{schema}.attractionprice.price >= 0")
    
    if general_requirements.get("Transportation"):
        if general_requirements["Transportation"] == "self-drive car":
            if table == "restaurant":
                conditions.append(f"{schema}.restaurant.parking_available = TRUE")
            elif table == "hotel":
                conditions.append(f"('Bãi đậu xe' = ANY({schema}.hotel.amenities) OR 'Garage' = ANY({schema}.hotel.amenities))")

    if general_requirements.get("District"):
        district = general_requirements["District"]
        if table == "hotel":
            conditions.append(f"unaccent(lower(({schema}.hotel.address).district)) ILIKE unaccent('%{district}%')")
        elif table == "restaurant":
            conditions.append(f"unaccent(lower(({schema}.restaurant.address).district)) ILIKE unaccent('%{district}%')")
        elif table == "touristattraction":
            conditions.append(f"unaccent(lower(({schema}.touristattraction.address).district)) ILIKE unaccent('%{district}%')")
    # Process specific requirements for each table
    if table == "hotel":
        if requirements.get("Style"):
            styles_condition = (" OR ".join([f"{schema}.hotel.style LIKE '{style}%'" for style in requirements["Style"]]))
            conditions.append(f"({styles_condition})")
    elif table == "restaurant":
        if requirements.get("Restaurant_Type"):
            conditions.append(f"'{requirements['Restaurant_Type']}' = ANY({schema}.restaurant.restaurant_type)")
        if requirements.get("Suitable_For"):
    # Nếu Suitable_For là một mảng, chúng ta cần sử dụng ANY với một array trong SQL
            if isinstance(requirements["Suitable_For"], list):
                suitable_for_values = ", ".join([f"'{item}'" for item in requirements["Suitable_For"]])
                conditions.append(f"({suitable_for_values}) = ANY({schema}.restaurant.suitable_for)")
            else:
                # Nếu chỉ có một giá trị, xử lý như chuỗi bình thường
                conditions.append(f"'{requirements['Suitable_For']}' = ANY({schema}.restaurant.suitable_for)")
    elif table == "touristattraction":
        if requirements.get("Attraction_Type"):
    # Kiểm tra xem 'Attraction_Type' có phải là một danh sách hay không
            if isinstance(requirements["Attraction_Type"], list):
                # Nếu là danh sách, ta xây dựng điều kiện với ANY
                attraction_condition = (" OR ".join([f"'{attraction_type}' = ANY({schema}.touristattraction.attraction_type)" for attraction_type in requirements["Attraction_Type"]]))
            else:
                # Nếu là chuỗi, chỉ cần so sánh trực tiếp với 'ANY'
                attraction_condition = f"'{requirements['Attraction_Type']}' = ANY({schema}.touristattraction.attraction_type)"
    
    # Thêm điều kiện vào danh sách conditions
        conditions.append(attraction_condition)

    # Build the WHERE clause and complete query
    where_clause = " AND ".join(conditions)

    # JSON SELECT queries for each table
    json_select = {
        "hotel": f"""
            json_build_object(
                'hotel_id', {schema}.hotel.hotel_id,
                'name', {schema}.hotel.name,
                'address', {schema}.hotel.address,
                'location', ST_AsGeoJSON({schema}.hotel.location)::json,
                'price', (
                    SELECT json_object_agg(room_type, price)
                    FROM {schema}.hotelprice
                    WHERE {schema}.hotelprice.hotel_id = {schema}.hotel.hotel_id
                ),
                'amenities', {schema}.hotel.amenities,
                'style', {schema}.hotel.style,
                'rating', {schema}.hotel.rating,
                'description', {schema}.hotel.description,
                'img_url', {schema}.hotel.img_url,
                'comments', {schema}.hotel.comments
            )
        """,
        "restaurant": f"""
            json_build_object(
                'res_id', {schema}.restaurant.res_id,
                'name', {schema}.restaurant.name,
                'address', {schema}.restaurant.address,
                'location', ST_AsGeoJSON({schema}.restaurant.location)::json,
                'working_hour', {schema}.restaurant.working_hour,
                'suitable_for', {schema}.restaurant.suitable_for,
                'restaurant_type', {schema}.restaurant.restaurant_type,
                'rating', {schema}.restaurant.rating,
                'description', {schema}.restaurant.description,
                'price_range', {schema}.restaurant.price_range,
                'average_price_per_person', ((CAST({schema}.{table}.price_range->>'min_price' AS INTEGER) + CAST({schema}.{table}.price_range->>'max_price' AS INTEGER)) / 2),
                'parking_available', {schema}.restaurant.parking_available,
                'kids_play_area', {schema}.restaurant.kids_play_area,
                'img_url', {schema}.restaurant.img_url,
                'comments', {schema}.restaurant.comments
            )
        """,
        "touristattraction": f"""
            json_build_object(
                'attraction_id', {schema}.touristattraction.attraction_id,
                'name', {schema}.touristattraction.name,
                'address', {schema}.touristattraction.address,
                'location', ST_AsGeoJSON({schema}.touristattraction.location)::json,
                'price', (
                    SELECT json_object_agg(ticket_type, price)
                    FROM {schema}.attractionprice
                    WHERE {schema}.attractionprice.attraction_id = {schema}.touristattraction.attraction_id
                ),
                'attraction_type', {schema}.touristattraction.attraction_type,
                'working_hour', {schema}.touristattraction.working_hour,
                'rating', {schema}.touristattraction.rating,
                'tour_duration', {schema}.touristattraction.tour_duration,
                'description', {schema}.touristattraction.description,
                'img_url', {schema}.touristattraction.img_url,
                'comments', {schema}.touristattraction.comments
            )
        """
    }

    query = (
        f"SELECT {json_select[table]} AS {table}_info "
        f"FROM {schema}.{table} {joins} "
        f"WHERE {where_clause};"
        if conditions else
        f"SELECT {json_select[table]} AS {table}_info FROM {schema}.{table};"
    )

    return query
    
    
def convert_to_json_format(results):
    """
    Convert the output format from [('JSON object',), ('JSON object',)] 
    to [{'key': value}, {'key': value}]
    """
    return [result[0] for result in results]
    
def fetch_locations(query, postgres_url):
    conn = psycopg2.connect(postgres_url)
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")
    # Thiết lập search_path
    cur.execute("""SET search_path TO travel_database, public;""")
    
    cur.execute(query)

    # Lấy tất cả các kết quả
    results = cur.fetchall()

    # Đóng kết nối
    cur.close()
    conn.close()

    return convert_to_json_format(results)
