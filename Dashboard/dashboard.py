import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    customers_df = pd.read_csv("Data/customers_dataset.csv")
    sellers_df = pd.read_csv("Data/sellers_dataset.csv")
    orders_df = pd.read_csv("Data/orders_dataset.csv")
    order_items_df = pd.read_csv("Data/order_items_dataset.csv")
    products_df = pd.read_csv("Data/products_dataset.csv")
    product_category_df = pd.read_csv("Data/product_category_name_translation.csv")  
    return customers_df, sellers_df, orders_df, order_items_df, products_df, product_category_df

customers_df, sellers_df, orders_df, order_items_df, products_df, product_category_df = load_data()

# Gabungkan dataset produk dengan kategori terjemahan
products_df = products_df.merge(product_category_df, on="product_category_name", how="left")

# Gabungkan order_items_df dengan produk
merged_df = order_items_df.merge(products_df, on="product_id", how="left")

# Title of the dashboard
st.title("E-commerce Analysis Dashboard")

# Section 1: Demografi Pelanggan
st.header("Pertanyaan 1: Demografi Pelanggan")
n_top_cities = st.slider("Pilih jumlah kota teratas:", min_value=5, max_value=20, value=10)
top_cities = customers_df["customer_city"].value_counts().head(n_top_cities)
fig, ax = plt.subplots()
sns.barplot(x=top_cities.index, y=top_cities.values, ax=ax, palette="Blues_d")
ax.set_title("Top Kota dengan Pelanggan Terbanyak (Sep 2016 - Okt 2018)")
ax.set_xlabel("Kota")
ax.set_ylabel("Jumlah Pelanggan")
plt.xticks(rotation=45)
st.pyplot(fig)
with st.expander('Insight'):
    st.write("""
             São Paulo dan Rio de Janeiro adalah kota dengan potensi pasar terbesar untuk e-commerce. Kota-kota lain seperti Belo Horizonte dan Brasília juga berperan penting meskipun jumlah pelanggan lebih sedikit. Jika ingin melakukan ekspansi bisnis e-commerce, strategi pemasaran bisa difokuskan di São Paulo dan Rio de Janeiro terlebih dahulu sebelum menjangkau kota-kota lainnya.
             """)

# Section 2: Demografi Seller
st.header("Pertanyaan 2: Demografi Seller")
n_top_seller_cities = st.slider("Pilih jumlah kota seller teratas:", min_value=5, max_value=20, value=10)
seller_city_counts = sellers_df["seller_city"].value_counts().head(n_top_seller_cities)
fig, ax = plt.subplots()
sns.barplot(x=seller_city_counts.index, y=seller_city_counts.values, ax=ax, palette="Oranges_d")
ax.set_title("Top Kota dengan Seller Terbanyak (Sep 2016 - Okt 2018)")
ax.set_xlabel("Kota")
ax.set_ylabel("Jumlah Seller")
plt.xticks(rotation=45)
st.pyplot(fig)
with st.expander('Insight'):
    st.write("""
             1. São Paulo memiliki jumlah seller terbanyak dengan 28.758 seller, jauh lebih tinggi dibandingkan kota lain.Hal ini menunjukkan bahwa São Paulo mungkin merupakan pusat bisnis utama dalam platform e-commerce ini.
2. Kota dengan jumlah seller terbanyak kedua, Ibitinga, memiliki 7.750 seller, yang jauh lebih kecil dibandingkan São Paulo. Setelah Ibitinga, jumlah seller di kota-kota lainnya jauh lebih merata, berkisar antara 2.200 - 3.000 seller.
3. Kota-kota seperti Curitiba, Santo André, Belo Horizonte, dan Rio de Janeiro memiliki jumlah seller yang cukup banyak, menunjukkan bahwa mereka juga merupakan pusat perdagangan yang signifikan. Perusahaan dapat mempertimbangkan ekspansi atau strategi pemasaran yang lebih kuat di kota-kota ini untuk meningkatkan transaksi.
             """)

# Section 3: Tren Jumlah Transaksi per Jam
st.header("Pertanyaan 3: Tren Jumlah Transaksi per Jam")
selected_hours = st.multiselect("Pilih jam transaksi yang ingin ditampilkan:", options=list(range(24)), default=list(range(24)))
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
hourly_transactions = orders_df['order_purchase_timestamp'].dt.hour.value_counts().sort_index()
hourly_transactions = hourly_transactions[hourly_transactions.index.isin(selected_hours)]
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hourly_transactions.index, y=hourly_transactions.values, marker='o', color='b', ax=ax)
ax.set_title('Tren Transaksi per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Transaksi')
plt.xticks(range(0, 24))
plt.grid(True)
st.pyplot(fig)
with st.expander('Insight'):
    st.write("""
             Tren Transaksi per Jam
1. Jumlah transaksi sangat rendah antara pukul 01:00 hingga 06:00. Hal ini karena sebagian pelanggan mungkin sedang tidur atau tidak aktif berbelanja online.
2. Jumlah transaksi mulai meningkat secara tajam setelah pukul 06:00, dengan lonjakan yang signifikan sekitar pukul 08:00 - 10:00. Ini bisa menunjukkan bahwa pelanggan mulai berbelanja setelah bangun tidur atau sebelum memulai aktivitas harian mereka.
3. Puncak transaksi terjadi antara pukul 11:00 hingga 16:00, dengan jumlah transaksi tertinggi sekitar pukul 12:00 - 14:00. Ini menunjukkan bahwa banyak pelanggan melakukan pembelian saat jam istirahat kerja atau makan siang.
4. Terjadi sedikit penurunan transaksi setelah pukul 16:00, kemungkinan karena orang-orang sedang dalam perjalanan pulang kerja atau sekolah.
5. Aktivitas transaksi kembali stabil di malam hari, dengan banyak pelanggan masih aktif berbelanja setelah pukul 19:00 hingga 22:00. Ini bisa mencerminkan kebiasaan pelanggan yang lebih santai saat berbelanja di malam hari setelah menyelesaikan aktivitas harian mereka.
6. Setelah pukul 22:00, jumlah transaksi mulai menurun kembali, kemungkinan karena banyak orang sudah mulai beristirahat.
             """)

# Section 4: Produk Paling Sering Dibeli
st.header("Pertanyaan 4: Produk Paling Sering Dibeli")
n_top_products = st.slider("Pilih jumlah produk teratas:", min_value=5, max_value=20, value=10)
top_products = merged_df["product_id"].value_counts().head(n_top_products).reset_index()
top_products.columns = ["product_id", "total_orders"]
top_products = top_products.merge(merged_df[["product_id", "product_category_name_english"]].drop_duplicates(), on="product_id", how="left")
top_products["product_label"] = top_products["product_category_name_english"] + " (" + top_products["total_orders"].astype(str) + ")"
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="total_orders", y="product_label", data=top_products, color="royalblue", ax=ax)
for i, value in enumerate(top_products["total_orders"]):
    ax.text(value + 2, i, str(value), va="center", fontsize=12)
ax.set_xlabel("Jumlah Transaksi")
ax.set_ylabel("Kategori Produk")
ax.set_title("Top Produk yang Paling Sering Dibeli (Sep 2016 - Okt 2018)")
st.pyplot(fig)
with st.expander('Insight'):
    st.write("""
            1. Produk dengan kategori bed_bath_table muncul dua kali di daftar dengan transaksi tertinggi (775 dan 488). Ini menunjukkan permintaan tinggi untuk produk kamar tidur dan kamar mandi.
2. Furniture_decor menempati posisi kedua (527 transaksi). Grden_tools muncul sebanyak empat kali dengan transaksi berkisar antara 373 hingga 484.
Ini menunjukkan bahwa pelanggan banyak membeli produk untuk mendekorasi rumah dan berkebun.
3. Computers_accessories (343 transaksi) menunjukkan bahwa aksesori komputer masih banyak dibeli. Watches_gifts (323 transaksi) menunjukkan adanya permintaan untuk produk fesyen & hadiah. Health_beauty (281 transaksi) mengindikasikan bahwa kategori kecantikan dan kesehatan juga cukup populer.
             """)

# Section 5: Kategori Produk Paling Banyak Terjual
st.header("Pertanyaan 5: Kategori Produk Paling Banyak Terjual")
n_top_categories = st.slider("Pilih jumlah kategori teratas:", min_value=5, max_value=20, value=10)
category_orders_df = merged_df.groupby("product_category_name_english").agg(
    total_orders=("order_id", "count")
).reset_index().sort_values(by="total_orders", ascending=False).head(n_top_categories)
fig, ax = plt.subplots()
sns.barplot(x=category_orders_df["total_orders"], y=category_orders_df["product_category_name_english"], ax=ax, palette="Greens_d")
for i, value in enumerate(category_orders_df["total_orders"]):
    ax.text(value + 2, i, str(value), va="center", fontsize=12)
ax.set_title("Top Kategori Produk yang Paling Banyak Terjual (Sep 2016 - Okt 2018)")
ax.set_xlabel("Jumlah Transaksi")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)
with st.expander('Insight'):
    st.write("""
            Kategori bed_bath_table mendominasi penjualan dengan 13.517 transaksi, diikuti oleh health_beauty (9.670) dan sports_leisure (8.641), menunjukkan tingginya minat pelanggan terhadap produk rumah tangga, kesehatan, dan olahraga. Kategori seperti furniture_decor dan computers_accessories juga cukup laris, mengindikasikan permintaan stabil untuk dekorasi rumah dan teknologi. Selain itu, housewares, watches_gifts, dan telephony menunjukkan potensi pertumbuhan yang dapat dimanfaatkan dengan strategi pemasaran yang tepat. Untuk meningkatkan penjualan, promosi dan bundling produk best seller, serta fokus pada tren kesehatan dan teknologi, dapat menjadi strategi yang efektif.
             """)
