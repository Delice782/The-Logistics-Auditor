# The "Last Mile" Logistics Auditor

### A. Executive Summary
An audit of 99,441 Olist e-commerce orders reveals that nearly 1 in 10 deliveries (9.6%) arrive after the promised date, directly driving negative customer reviews. Super Late deliveries (5+ days past estimate) receive an average review score of just 1.86 out of 5, compared to 4.30 for on-time deliveries, a 2.44-point collapse in customer satisfaction. The problem is not nationwide as it is concentrated in Brazil's north and northeast, where Alagoas (AL) records a 27.2% late delivery rate more than double the national average of 11.78%. Analysis also shows that late rates spike during peak months like November and February, suggesting the logistics network hits a fixed capacity ceiling under high demand. The core finding is clear: Veridi is over-promising and under-delivering to specific regions and during specific seasons, and the customer reviews prove it.

### B. Project Links
Notebook: https://colab.research.google.com/drive/19AI4R11tRqu7kHqKNaDhJySBE_xOh--K?usp=sharing

Dashboard: 

Presentation: https://www.canva.com/design/DAHE3GBpLWE/KiKAOq8yDV4iz8-efMEmng/edit?utm_content=DAHE3GBpLWE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Video Walkthrough: 

### C. Technical Explanation

#### Data Cleaning
Six CSV files were loaded using a relative path helper function that checks both the current directory and /content for Google Colab compatibility, ensuring full reproducibility regardless of environment. Before joining, the reviews table was aggregated by order_id to prevent row duplication caused by multiple reviews per order, which is a common source of inflated row counts in 1-to-many joins. Date columns were cast to datetime before calculating days_difference as the estimated date minus the actual delivery date. Orders with missing delivery dates and those with a status of canceled or unavailable (2,971 orders total) were flagged as Excluded and removed from all analysis, leaving 96,470 clean delivered orders.

#### Candidate's Choice: Monthly Delivery Trend Analysis
A dual-axis monthly chart was added to track total order volume and late delivery rate side by side over time. This feature matters to the business because it exposes the relationship between demand spikes and logistics failure: late rates jumped to 16.2% during the November 2017 Black Friday peak and climbed further to 23.85% in March 2018 despite lower volumes. This pattern reveals that Veridi's network has a fixed capacity ceiling and the same delivery promise that works in July breaks in November. The business implication is actionable: implement dynamic delivery windows that automatically add 5 to 7 buffer days during historically high-risk months rather than applying a single nationwide estimate year-round.

Dataset: Kaggle - Olist Brazilian E-Commerce Dataset (https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
