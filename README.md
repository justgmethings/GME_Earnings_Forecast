# GME Earnings Forecast for Q2 ’25 and FY ’25

---

**I am not a financial analyst, and this is not financial advice. Please do your own due diligence. All equity investing comes with risks.**

---

Archived Earnings Forecasts:

- [Q2 ’25 and FY ’25](https://github.com/justgmethings/GME_Earnings_Forecast/blob/main/archive/earnings_forecast_q2-2025.md)

## UPDATE: Q2 ‘25 Estimates Versus Results
*All estimates reported in millions of US dollars.*
| |Q2 ‘25 Estimated|Q2 ‘25 Reported|Pct. Error|
|:-|:-|:-|:-|
|Net Sales|886.44|972.2|+8.8%|
|Cost of Sales|630.41|689.1|+8.5%|
|SG&A|198.76|218.8|+9.2%|
|Asset Impairments|0.00|2.1|+100%|
|Operating Income|57.27|66.4|+13.8%|
|Operating Income (Excl. Asset Impairments)|57.27|64.3|+10.9%|
|Interest Income|(80.44)|(79.6)|-1.1%|
|Other Income|(28.90)|(28.6)|-1.0%|
|Income Tax Expense|13.77|6.0|-130.5%|
|Net Income|152.84|168.6|+9.3%|

*Notes: ‘Other Income’ incorporates forecasted BTC earnings for Q2 ’25. Relative to the original table, I switched the location of "Operating Income" and "Asset Impairments" to better reflect that asset impairments are included in operating income. I've also changed the formatting to wrap interest income and other income to indicate negative values as it is reflected in the GME earnings statement.*

<br>

**Percentage of Net Sales:**

*Comparison of estimated values as a percentage of estimated net sales versus reported values as a percentage of reported net sales.*
| |Q2 ‘25 Estimated|Q2 ‘25 Reported|Pct. Error|
|:-|:-|:-|:-|
|Net Sales|100%|100%|n/a|
|Cost of Sales|71.1%|70.9%|-.3%|
|SG&A|22.4%|22.5%|-.4%|
|Net Income|17.2%|17.3%|-.6%|


## TL;DR

I build a forecast model of GameStop’s earnings for the remainder of FY ’25. I attempt to build my model around estimates of the future sales, costs, and interest earnings of the company as it exists in Q2 ’25. This means I do not include potential future earnings based on, for example, new revenue initiatives, additional cash earned from future stock sales or convertible bonds, profits/losses on Bitcoin outside of Q2, or future changes in the macroeconomy. I estimate net sales of $886 million and $3.868 billion in Q2 ’25 and FY ’25, respectively and earnings per share of $0.342 and $1.230 in Q2 ’25 and FY ’25, respectively.


## Introduction

I project GameStop’s (referred to as “the company” or “GME” throughout) earnings for Q2 2025 (results will be reported on 9/9/2025), as well as for the entirety of FY 2025. My goal with this exercise is to produce a reasonable, conservative estimate of GME’s future earnings based on its *existing* operations, and not speculation about future initiatives, new financial vehicles to raise funds for the company, or the future path of Bitcoin. This means I do not provide projections for future/novel revenue streams (other than the Switch 2), like the new digital Power Packs. My estimates also implicitly assume stability in the macro environment. This cannot be taken for granted but attempting to forecast macroeconomic volatility (to the upside or downside) is beyond the scope of this analysis.

I take a bottom-up approach to my forecast by projecting sales and costs for each regional business unit and aggregating those estimates up to projections for the full company. This will ideally produce a better forecast since the trend for each segment is different and GME sold its Canadian operations in Q1 2025 (i.e., projecting from total company operations will erroneously include past Canadian sales). I then layer on my projections for Switch 2 hardware and software sales to produce an estimate of total company-wide sales and operating costs. I also implement and back-test an interest rate model to forecast my base case for interest earnings. I estimate likely BTC earnings based on the timing of the purchase, public statements, and the end of quarter price of BTC in Q2 ‘25. Finally, I assume that GME pays a 10% tax rate on operating income and interest income.

*All models are wrong, but some are useful – George Box*


## Stipulations

My forecast is based on a series of assumptions (as described in the Appendix below) tailored to what I estimate as the most likely outcome for earnings. However, I do not place a specific probability on that outcome, nor a probability distribution on the range of potential outcomes. My model may be missing important elements of the company’s operations, or get important elements wrong, which will cause my model to overestimate or underestimate earnings. I also make no claims about the fair value of GME, the future direction of the share price, or the ultimate impact of the company’s earnings on the share price. **These estimates should not be misconstrued as an endorsement for or against the stock or a recommendation for a particular investment strategy.**


## Forecast
<br>

**Net Sales Forecast**

Q2 ’25: $886 million (+11% YoY)

FY ’25: $3.868 billion (+1% YoY)   
<br>

**EPS Forecast**

Q2 ’25: $0.342 (+793% YoY)

FY ’25: $1.230 (+269% YoY)

*Note: Based on 447.3 million shares outstanding.*  
<br>

**Detailed Earnings Forecast**

*All estimates reported in millions of US dollars.*
| |Q2 ‘25|FY ‘25|
|:-|:-|:-|
|Net Sales|886.44|3868.49|
|Cost of Sales|630.41|2690.36|
|SG&A|198.76|872.72|
|Operating Income|57.27|305.42|
|Asset Impairments|0.00|-35.50|
|Interest Income|80.44|305.36|
|Other Income|28.90|31.10|
|Income Tax Expense|13.77|56.42|
|Net Income|152.84|549.96|

*Notes: ‘Other Income’ incorporates forecasted BTC earnings for Q2 ’25.*

 

## Appendix

**What are the key assumptions to my forecast?**

* **Regional sales:** First, I calculate the YoY percent growth in net sales in each of Q1 ’24 and Q1 ‘25 for each of the regional business units – the United States (US), Australia/New Zealand (AU), and Europe (EU, which now only includes France) to project future quarters of revenue. For the US, Q1 ’24 to Q1 ’25 net sales growth went from -25.84% to -12.93%, respectively, or a change of +12.91 percentage points. I leverage this percentage point improvement to forecast future net sales. Specifically, I conservatively assume that the YoY percent growth in net sales improve by 10 percentage points (versus the 12.91 percentage point improvement calculated above) in Q2, Q3, and Q4 of ’25 relative to the same quarters in ’24. This yields -18%, -10%, and -15% YoY growth in net sales in Q2, Q3, and Q4 of ’25, respectively. For AU, the Q1 ’25 YoY growth in net sales was +2.89%. For future quarters, I conservatively assume that net sales improve such that the YoY growth in Q2, Q3, and Q4 of ’25 is +0%. For the EU, the Q1 ’25 YoY growth in net sales was -47.43%. For future quarters, I assume a +5 percentage point improvement in YoY growth in net sales. This yields YoY growth in net sales of -35%, -17%, and -42% in Q2, Q3, and Q4, respectively. Given the growth in the collectibles category and the foot traffic being driven by the restart of the console cycle (see discussion of Switch 2 sales, which are modeled separately, below), I maintain that these estimates are more likely to be too low than too high. However, Q1 ’25 was an exceptionally good quarter, and there are obviously risks with extrapolating from this one data point. Therefore, taking a more conservative posture with these projections is prudent.
* **Regional cost of sales:** The primary challenge with forecasting cost of sales for each regional business unit (US, AU, and EU) is that GME did not report quarterly cost of sales for FY ’24 disaggregated by business unit. However, company-wide quarterly cost of sales is available. I calculate a scaling factor for each quarter based on the company-wide quarterly cost of sales data. Specifically, I divide the FY ’24 cost of sales (normalized as a percentage of net sales) for each business unit by the company-wide FY ’24 cost of sales (again, normalized). I then multiply each of these region-specific scaling factors by the company-wide (normalized) cost of sales in Q2, Q3, and Q4 of FY ’24 to obtain an estimate of (normalized) cost of sales in each regional business unit for Q2, Q3, and Q4 of FY ’24. This is imperfect since there was certainly quarter-by-quarter variation in cost of sales for each regional business unit not captured by the company-wide quarter-by-quarter variation in cost of sales. However, it provides a rough estimate for regional figures and it is likely a better representation for the US, which is the largest regional unit and counts for the bulk of the costs of sales, than other regions. Next, I need to convert these regional Q2, Q3, and Q4 estimates of (normalized) cost of sales in FY ’24 into forecasts for the same quarters in FY ’25. Fortunately, GME produced cost of sales figures for Q1 ’25 and Q1’ 24 for each regional business unit in the Q1 ‘25 earnings statement. I use these figures to calculate the YoY percent change in (normalized) cost of sales for each regional business unit in Q1 ’25. In the US, AU, and EU the YoY percent change in (normalized) cost of sales as -12%, .1%, and -3.2%, respectively. I revise these estimates to -10%, +0%, and -1% to reflect a more conservative projection. I divide by 100 and add 1 to each of these revised estimates and then multiply these figures by the previously calculated regional (normalized) cost of sales estimates for Q2, Q3, and Q4 of FY ’24 to produce projections for the (normalized) cost of sales in each regional business unit in the corresponding quarters in FY ’25. Finally, multiplying these (normalized) cost of sales projections for FY ’25 by my previous projections for total sales in each regional business unit yields the final forecast of cost of sales in dollars for Q2, Q3, and Q4 in each region. Ultimately, the YoY percent change in (normalized) cost of sales in Q1 ’25 is likely a reasonable estimate of the same figures for the remaining quarters of the year because historical earnings results show that (normalized) cost of sales are relatively stable in Q2, Q3, and Q4 of a given fiscal year relative to Q1 of the same fiscal year.
* **Regional SG&A:** My methodology for SG&A follows the same procedure as that of cost of sales. As with cost of sales, these calculations require normalization of SG&A with net sales. One important note is that (normalized) SG&A is not as consistent throughout the year as (normalized) cost of sales. Specifically, Q4 generally comes in at a lower value than preceding quarters. In recent years it has come in at a company-wide normalized figure of \~.2-.22. Therefore, I artificially adjust the assumption for YoY percent change in Q4 ’25 to minimize projected changes compared to Q4 ’24, such that my projection is closer to \~.20 (with variance depending on the region). One simple way to judge whether this approach is reasonable is to ask whether the YoY percent change in (normalized) SG&A for Q1 ’25 could be sustained for the remaining quarters in FY ’25. These figures for the US, AU, and EU are -5.2%, -8.5%, and -19.7%, respectively. On their face, these numbers seem like large declines. However, it is important to keep in mind that these Q1 ’25 estimates represent a “reversion to the mean” for (normalized) SG&A after large YoY percent increases in each region in FY ’24 of +17.1%, +17.5%, and +19.9% in the US, AU, and EU, respectively. Especially for the US, this was likely associated with substantial fixed costs for staff to develop new (forthcoming) revenue streams (e.g., digital Power Packs). Given the one-time up-front nature of these kind of investments, management’s prioritization of efficiency and cost-cutting, and the historic consistency of YoY percent change in (normalized) SG&A across Q1, Q2, and Q3 of this year, I maintain that the Q1 ’25 YoY percent change in (normalized) SG&A for each regional business unit is reasonable.
* **Estimate of Total Switch 2 Sales in US:** Reported Switch 2 sales in the US were [1.62 million in June ’25](https://www.vgchartz.com/article/465278/switch-2-vs-switch-1-sales-comparison-in-the-us-june-2025/) and [457k in July ’25](https://www.vgchartz.com/article/465596/switch-2-best-seller-as-sales-near-25m-americas-hardware-estimates-for-july-2025/). [Projections](https://www.ainvest.com/news/nintendo-switch-2-launch-faces-trade-war-headwinds-2504/) are for 4.6 million in Switch 2 sales in CY 25. I distribute the projected Switch 2 sales for the remainder of the year based partially on Switch 1 sales, with greater sales volume in the holiday season. Specifically, I assume 720k will be sold in the US in August, September, and October (Q3) and 2.45 million sold in the US in November, December, and January (Q4). I assume that 2.5 games and 1.5 accessories are sold for each Switch 2 in FY ’25 in the US. I assume a weighted cost of Switch 2 consoles, games, and accessories of $450, $72.50, and $70, respectively.
* **Switch 2 sales by GME:** I assume that GME will capture 15% of U.S. Switch 2 sales in each quarter of FY ’25. One GME store posted that it had [83 Switch 2 consoles](https://comicbook.com/gaming/news/gamestop-nintendo-switch-2-pre-order-allocations-warning/) available for pre-order. If we round up to 90 and multiply by 2,325 stores across the US. That equals 209,250 Switch 2 consoles or \~13% of all Switch 2’s sold in June. Obviously, one store is a small *n* to use for the Switch 2 projections. [Based on industry data](https://www.theesa.com/u-s-consumer-spending-on-video-games-totaled-58-7-billion-in-2024/) and GME’s FY ’24 earnings statement, GME accounted for approximately 26% of total gaming hardware/accessory sales in the US ($2.1 billion out of $8.1 billion). Furthermore, [public reports](https://www.tomshardware.com/video-games/handheld-gaming/nintendo-reportedly-pulled-products-including-switch-2-from-amazon-u-s-because-of-alleged-sales-dispute-both-companies-deny-claims) indicate that a major retailer was excluded from the first month of Switch 2 sales. Given this data, selecting a more aggressive estimate of 15% for GME’s share of Switch 2 sales seems reasonable. I assume a gross margin of 2.5% on Switch 2 consoles, 25% on Switch 2 games, and 25% on Switch 2 accessories. And I add a small 2% cost to reflect increased SG&A associated with the Switch 2 release (e.g., advertising). These components allow me to forecast total costs and total revenue from Switch 2 consoles, accessories, and software in the US. I forecast AU and EU Switch 2 sales based on the relative population and GDP per capita of each of the countries represented in each of the regional business units relative to the US to get a “scaled” version of Switch 2 sales in each region outside the US. In total, I project $25 million and $89 million in total net income associated with sales of Switch 2 consoles, accessories, and software in Q2 ’25 and FY ’25, respectively.
* **Interest rates:** I assume that the company receives a 4.4% annual yield on its cash holdings in Q2 ‘25. Based on the prevailing market probabilities at the time of the forecast, I assume a 25 basis point interest rate cut at the Federal Reserve’s September meeting and another 25 basis point cut at its October meeting.
* **Interest earnings:** I do not estimate the *additional* interest earnings accrued from future operating profits (e.g., interest earned in Q2, Q3, and Q4 of ’25 from unspent operating profits in Q2 ’25). This is simply done to improve the simplicity and tractability of my interest earnings model; however, it is a notable omission given my projections for operating income and, all else equal, will likely lead to my model underestimating interest income in FY 2025. I implicitly assume that there are no additional stock sales or convertible bonds that increase the company’s cash reserves.
* **BTC earnings:** I assume that the company’s Bitcoin cost basis is $106.4k per BTC. With 4,710 BTC’s purchased, this represents $501.1 million spent on BTC in Q1 ’25. This is in line with public statements given by the CEO to CNBC, which stated that the company purchased “just over 500 million dollars” in BTC. I use an end-of-quarter value for BTC of $112.5k, which corresponds with an estimate of $28.9 million in BTC gains for Q2 ’25. While BTC is historically volatile, I project no change (gain or loss) in the value of the cryptocurrency in Q3 and in Q4, which reflects my uncertainty over its future direction. Obviously, others will disagree, and this is an easy assumption to adjust to reflect your preferred earnings estimate based on your own forecasted path for BTC. BTC earnings are reflected in “Other Income”. The only other contribution to “Other Income” in my forecast is from Q1 ’25 and is reflected in the “Other Income” forecast for FY ’25.
* **French operations:** I assume that the remaining EU operation (i.e., France) is not sold until the end of the fiscal year. I base this on two data points. First, in its Q2 ’25 earnings statement, the company states that “The sale of the operations in France is expected to close during fiscal year 2025.” Second, the company will likely be aiming for YoY revenue growth in FY ’25, and it is noteworthy that the timing of the sale may ultimately determine whether GME reaches that goal. My base case is for net sales of $3.868 billion in FY ‘25. In FY ’24, reported net sales were $3.823 billion. In Q1 ’25 the French operations brought in $74.8 million. If you assume constant revenue for the French operations for the remainder of the year, losing even one quarter of the French operations would result in negative YoY growth in revenue for the entire company. A more complex implementation of this exercise via my earnings model yields a similar story: company-wide net sales would be $3,754.24 in FY ’25 without the French operations in Q4 ’25. Of course, it is also worth noting that there is a tradeoff between the top- and bottom-lines in this case – the French operations can pad revenues at the cost of net income.
* **Sale of Canadian operations:** I assume no net proceeds in Q2 ’25 from the sale of the Canadian operations. This is probably an underestimate, but my assumption is that it will not materially affect earnings.
* **Taxes:** I have low confidence in this estimate and primarily relied on ChatGPT to try to come to a reasonable forecast. I assume a uniform 10% tax on operating income and interest earned.
