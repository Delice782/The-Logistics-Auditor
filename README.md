# The "Last Mile" Logistics Auditor

### A. Executive Summary
An audit of 94,496 Olist e-commerce orders reveals that nearly 1 in 10 deliveries (8%) arrive after the promised date, directly driving negative customer reviews. Super Late deliveries (5+ days past estimate) receive an average review score of just 1.86 out of 5, compared to 4.29 for on-time deliveries, a 2.43-point collapse in customer satisfaction. The problem is not nationwide as it is concentrated in Brazil's north and northeast, where Alagoas (AL) records a 27.2% late delivery rate more than double the national average of 11.78%. Analysis also shows that late rates spike during peak months like November and March, suggesting the logistics network hits a fixed capacity ceiling under high demand. The core finding is clear: Veridi is over-promising and under-delivering to specific regions and during specific seasons, and the customer reviews prove it.

### B. Project Links
Notebook: https://colab.research.google.com/drive/19AI4R11tRqu7kHqKNaDhJySBE_xOh--K?usp=sharing

Dashboard: https://the-logistics-auditor-cxnaive8z42zbtybnxpt6s.streamlit.app/

Presentation: https://drive.google.com/file/d/1Z-k3eTEzym_t7zDq7ddxqKhoGVyZMFYI/view?usp=sharing

### C. Technical Explanation

#### Data Cleaning
Six CSV files were loaded using a relative path helper function that checks both the current directory and /content for Google Colab compatibility, ensuring full reproducibility regardless of environment. Before joining, the reviews table was aggregated by order_id to prevent row duplication caused by multiple reviews per order, which is a common source of inflated row counts in 1-to-many joins. Date columns were cast to datetime before calculating days_difference as the estimated date minus the actual delivery date. Orders with missing delivery dates and those with a status of canceled or unavailable (2,819 orders total) were flagged as Excluded and removed from all analysis, leaving 96,470 clean delivered orders.

#### Candidate's Choice: Monthly Delivery Trend Analysis
This analysis tracks how late delivery rates change month by month alongside total order volume. Veridi applies the same delivery estimate regardless of the time of year, but the data shows that the logistics network cannot maintain consistent performance during high demand periods. Late delivery rates spiked to 16.2% in November 2017 and rose even higher to 23.85% in March 2018, while the baseline rate in quieter months sits around 8%. This gap between peak and off-peak performance reveals a capacity problem that a fixed delivery promise cannot absorb. Veridi needs to implement seasonal delivery windows that automatically extend estimates by 5 to 7 days during historically high-risk months so that customers receive honest timelines instead of broken promises.

Dataset: Kaggle - [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
