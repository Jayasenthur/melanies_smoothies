# Import python packages
import streamlit as st

# App title
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be', name_on_order)

# Snowflake connection
cnx = st.connection('snowflake')
session = cnx.session()

# Get fruit options (NO snowpark.functions import)
fruit_df = (
    session
    .table("smoothies.public.fruit_options")
    .select("FRUIT_NAME")
    .collect()
)

fruit_list = [row["FRUIT_NAME"] for row in fruit_df]

# Multiselect
ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Insert order
if ingredient_list and name_on_order:
    ingredients_string = ' '.join(ingredient_list)

    if st.button('Submit Order'):
        session.sql(
            """
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES (?, ?)
            """,
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

