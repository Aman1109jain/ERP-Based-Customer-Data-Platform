import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# DATABASE CONNECTION -- edit these to match your local setup
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1109_J@in_aman",
    "database": "erp_cdp_system",
}

st.set_page_config(page_title="ERP Console", layout="wide")

@st.cache_resource
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def run_query(sql):
    conn = get_connection()
    try:
        return pd.read_sql(sql, conn)
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


# HEADER
st.title("ERP / CDP Dashboard")
st.caption("erp_cdp_system — live view")

if st.button("Refresh data"):
    st.cache_resource.clear()
    st.rerun()

# KPIs
kpi_df = run_query(
    """
    SELECT
        (SELECT COUNT(*) FROM cdp)                                              AS totalCustomers,
        (SELECT COUNT(*) FROM salesOrder)                                       AS totalOrders,
        (SELECT COALESCE(SUM(totalAmount),0) FROM salesOrder)                   AS totalRevenue,
        (SELECT COUNT(*) FROM product)                                         AS totalProducts,
        (SELECT COUNT(*) FROM supplier)                                        AS totalSuppliers,
        (SELECT COUNT(*) FROM inventory WHERE quantityInStock <= reorderLevel) AS lowStockCount,
        (SELECT COALESCE(AVG(totalAmount),0) FROM salesOrder)                   AS avgOrderValue,
        (SELECT COUNT(*) FROM salesOrder WHERE paymentStatus='Pending')         AS pendingPayments
    """
)

if not kpi_df.empty:
    k = kpi_df.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers", f"{int(k.totalCustomers):,}", f"{int(k.totalSuppliers)} suppliers")
    c2.metric("Total Revenue", f"₹{k.totalRevenue:,.0f}", f"avg ₹{k.avgOrderValue:,.0f}/order")
    c3.metric("Orders", f"{int(k.totalOrders):,}", f"{int(k.pendingPayments)} pending payment")
    c4.metric("Products", f"{int(k.totalProducts):,}", f"{int(k.lowStockCount)} low stock", delta_color="inverse")

st.divider()

# REVENUE TREND + CATEGORY / SEGMENT MIX
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader("Revenue Trend (monthly)")
    trend_df = run_query(
        """
        SELECT DATE_FORMAT(orderDate, '%Y-%m') AS month,
               SUM(totalAmount) AS revenue,
               COUNT(*) AS orders
        FROM salesOrder
        GROUP BY month
        ORDER BY month
        """
    )
    if not trend_df.empty:
        fig = px.area(trend_df, x="month", y="revenue")
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=320)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sales by Category")
    cat_df = run_query(
        """
        SELECT p.category AS category, SUM(sd.totalPrice) AS revenue
        FROM salesDetails sd
        JOIN product p ON p.productID = sd.productID
        GROUP BY p.category
        ORDER BY revenue DESC
        """
    )
    if not cat_df.empty:
        fig = px.pie(cat_df, names="category", values="revenue", hole=0.5)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=320)
        st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader("Customer Segments")
    seg_df = run_query("SELECT customerSegment AS segment, COUNT(*) AS count FROM cdp GROUP BY customerSegment")
    if not seg_df.empty:
        fig = px.pie(seg_df, names="segment", values="count", hole=0.5)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=320)
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# PRODUCTS + FULFILLMENT
col4, col5, col6 = st.columns([2, 1, 1])

with col4:
    st.subheader("Top 10 Products by Revenue")
    top_products_df = run_query(
        """
        SELECT p.productName AS productName,
               SUM(sd.quantity) AS unitsSold,
               SUM(sd.totalPrice) AS revenue
        FROM salesDetails sd
        JOIN product p ON p.productID = sd.productID
        GROUP BY sd.productID
        ORDER BY revenue DESC
        LIMIT 10
        """
    )
    if not top_products_df.empty:
        fig = px.bar(top_products_df.sort_values("revenue"), x="revenue", y="productName", orientation="h")
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=340)
        st.plotly_chart(fig, use_container_width=True)

with col5:
    st.subheader("Delivery Status")
    delivery_df = run_query("SELECT deliveryStatus AS status, COUNT(*) AS count FROM salesOrder GROUP BY deliveryStatus")
    if not delivery_df.empty:
        fig = px.pie(delivery_df, names="status", values="count")
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=340)
        st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Production Status")
    prod_df = run_query("SELECT status, COUNT(*) AS count FROM production GROUP BY status")
    if not prod_df.empty:
        fig = px.bar(prod_df, x="status", y="count", color="status")
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=340, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# WATCHLISTS
col7, col8 = st.columns(2)

with col7:
    st.subheader(" Low Stock Alerts")
    low_stock_df = run_query(
        """
        SELECT p.productName AS Product,
               i.warehouseLocation AS Warehouse,
               i.quantityInStock AS `In Stock`,
               i.reorderLevel AS `Reorder At`
        FROM inventory i
        JOIN product p ON p.productID = i.productID
        WHERE i.quantityInStock <= i.reorderLevel
        ORDER BY (i.quantityInStock - i.reorderLevel) ASC
        LIMIT 20
        """
    )
    if low_stock_df.empty:
        st.info("Nothing below reorder level.")
    else:
        st.dataframe(low_stock_df, use_container_width=True, hide_index=True)

with col8:
    st.subheader(" Top Customers by Spend")
    top_customers_df = run_query(
        """
        SELECT CONCAT(c.firstName, ' ', c.lastName) AS Customer,
               c.customerSegment AS Segment,
               COUNT(so.orderID) AS Orders,
               SUM(so.totalAmount) AS `Total Spent`
        FROM salesOrder so
        JOIN cdp c ON c.customerID = so.customerID
        GROUP BY so.customerID
        ORDER BY `Total Spent` DESC
        LIMIT 10
        """
    )
    if not top_customers_df.empty:
        st.dataframe(top_customers_df, use_container_width=True, hide_index=True)

st.divider()

# RECENT ORDERS
st.subheader("Recent Orders")
recent_df = run_query(
    """
    SELECT so.orderID AS `Order #`,
           CONCAT(c.firstName, ' ', c.lastName) AS Customer,
           so.orderDate AS Date,
           so.totalAmount AS Amount,
           so.paymentStatus AS Payment,
           so.deliveryStatus AS Delivery
    FROM salesOrder so
    JOIN cdp c ON c.customerID = so.customerID
    ORDER BY so.orderID DESC
    LIMIT 15
    """
)
if not recent_df.empty:
    st.dataframe(recent_df, use_container_width=True, hide_index=True)

st.caption("Data refreshes when you click 'Refresh data' above, or restart the app.")