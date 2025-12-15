import streamlit as st
import snowflake.connector

st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

st.write(st.secrets)

name_on_order = st.text_input("Name on Smoothie:")

# Snowflake connection using secrets
conn = snowflake.connector.connect(
    account=st.secrets["snowflake"]["account"],
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"],
    role=st.secrets["snowflake"]["role"],
)

cur = conn.cursor()

# Fetch fruit options
cur.execute("SELECT FRUIT_NAME FROM FRUIT_OPTIONS")
fruit_list = [row[0] for row in cur.fetchall()]

ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

if ingredient_list and name_on_order:
    ingredients_string = " ".join(ingredient_list)

    if st.button("Submit Order"):
        cur.execute(
            """
            INSERT INTO ORDERS (ingredients, name_on_order)
            VALUES (%s, %s)
            """,
            (ingredients_string, name_on_order)
        )
        conn.commit()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")

cur.close()
conn.close()
