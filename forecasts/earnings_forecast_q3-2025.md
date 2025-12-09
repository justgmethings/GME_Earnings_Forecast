# GME Earnings Forecast for Q3 2025 and FY 2025

---

**I am not a financial analyst, and this is not financial advice. Please do your own due diligence. All equity investing comes with risks.**

---

## Q3 ‘25 Estimates

## TL;DR

I build a forecast model of GameStop’s earnings for Q3 2025 and FY 2025.  I attempt to build my model around estimates of the future sales, costs, and interest earnings of the company as it exists in Q3 2025. This means I do not include potential future earnings based on, for example, expectations of future revenue initiatives, additional cash earned from future stock sales or convertible bonds, profits/losses on Bitcoin outside of Q3, or future changes in the macroeconomy. I estimate net sales of $1.309 billion and $5.222 billion in Q3 2025 and FY 2025, respectively, and earnings per share of $0.263 and $1.491 in Q3 2025 and FY 2025, respectively.


## Introduction

I project GameStop’s (referred to as “the company” or “GME” throughout) earnings for Q3 2025 (results will be reported on 12/9/2025), as well as for the remainder of FY 2025. My FY 2025 estimates incorporate the reported results of earnings by GME for Q1 and Q2 of 2025 (i.e., the actual earnings for these quarters) and to my forecast for Q3 and Q4 of 2025. My goal with this exercise is to produce a reasonable, conservative estimate of GME’s future earnings based on its *existing* operations, and not speculation about future initiatives, new financial vehicles to raise funds for the company, or the future path of Bitcoin. I do not provide forecasts for future/novel revenue streams, other than the Switch 2; however, as of Q3, I do incorporate estimates of earnings for the new digital PowerPacks initiative via estimates from a [forecast](https://www.reddit.com/r/Superstonk/comments/1p8qeuz/2025_q3_earnings_forecast_power_packs_edition/) provided by u/regionformal on r/Superstonk, which is likely the most reliable publicly-available estimate on the likely earnings impact from this initiative. Still, due to the novel nature of the program, there is a high degree of uncertainty regarding the earnings for this initiative. Specifically, it is both difficult to determine ex-ante the magnitude of GME's sales/income from PowerPacks and how these numbers will be incorporated into the earnings statement (e.g., the accounting method GME will use for determining net sales from PowerPacks). I assume no growth in PowerPacks from Q3 to Q4. My estimates also implicitly assume stability in the macro environment. This cannot be taken for granted but attempting to forecast macroeconomic volatility (to the upside or downside) is beyond the scope of this analysis.

I take a bottom-up approach to my forecast by projecting sales and costs for each regional business unit and aggregating those estimates up to projections for the full company. This will ideally produce a better forecast since the trend for each segment is different and GME sold its Canadian operations in Q1 2025 (i.e., projecting from total company operations will erroneously include past Canadian sales, as well as certain country units that have recently been shuttered). I then layer on my projections for Switch 2 hardware and software sales to produce an estimate of total company-wide sales and operating costs. I also implement and back-test an interest rate model to forecast my base case for interest earnings. I estimate likely BTC earnings based on the timing of the purchase, public statements, and the end of quarter price of BTC in Q3 2025. Finally, I have revised my tax model for GME as of this quarter, as this was the worst-performing category of my Q2 2025 model on a percentage basis. In certain instances, I update the assumptions used in my Q3 and Q4 2025 forecast for net sales, cost of sales, and SG&A based on a calibration exercise that seeks to align my model for Q2 2025 with the reported results for that quarter (these instances are noted in the Appendix below).

## Stipulations

*All models are wrong, but some are useful – George Box*

My forecast is based on a series of assumptions (as described in the Appendix below) tailored to what I estimate as the most likely outcome for earnings. However, I do not place a specific probability on that outcome, nor a probability distribution on the range of potential outcomes. My model may be missing important elements of the company’s operations, or get important elements wrong, which will cause my model to overestimate or underestimate earnings. I also make no claims about the fair value of GME, the future direction of the share price, or the ultimate impact of the company’s earnings on the share price. **These estimates should not be misconstrued as an endorsement for or against the stock or a recommendation for a particular investment strategy.**

**_NOTE: While the numbers below constitute my forecast for the quarter, I am providing the following results showing topline and bottomline forecasts if PowerPacks earnings are omitted. Net Sales: $934.36 million. Net Income: $100.82 million. EPS: 0.225 million._**

## Forecast
<br>

**Net Sales Forecast**

Q3 2025: $1.309 billion (+52.2% YoY)

FY 2025: $5.222 billion (+36.6% YoY)
<br>

**Basic EPS Forecast**

Q3 2025: $0.263 (+657.5% YoY)

FY 2025: $1.491 (+352% YoY)

*Note: Based on 447.4 million shares outstanding.*  
<br>

**Normalized EPS Forecast**

Q3 2025: $0.237 (+295% YoY)

*Note: Based on diluted shares outstanding of 546.5 million shares.*  
<br>

**Detailed Earnings Forecast**

*All estimates reported in millions of US dollars.*
| |Q3 ‘25|FY ‘25|
|:-|:-|:-|
|Net Sales|1,309.36|5,221.94|
|Cost of Sales|993.21|3,826.06|
|SG&A|263.25|962.70|
|Asset Impairments|0.00|33.40|
|Operating Income|52.90|399.79|
|Interest Income|85.88|285.55|
|Other Income|0|2.20|
|Unrealized gain on digital assets|-11.60|17.00|
|Income Tax Expense|9.36|37.61|
|Net Income|117.82|666.93|

*Notes: I have moved the unrealized gain (loss) on BTC from ‘Other Income’ to "Unrealized gain on digital assets" for Q3 2025.*

 

## Appendix

**What are the key assumptions to my forecast?**

* **Regional Sales:** My methodology for forecasting net sales in the US remains the same in Q3 and Q4 2025 as it was in Q2 2025. I first calculate the YoY percent growth in net sales in each of Q1 2024 and Q1 2025. Q1 2024 to Q1 2025 net sales growth went from -25.84% to -12.93%, respectively, or a change of +12.91 percentage points. Based on this calculated percentage point improvement, I conservatively assume that the YoY percent growth between Q3 2024-->Q3 2025 and Q4 2024-->Q4 2025 in the US unit improved by 10 percentage points. This yields -10% and -15% YoY percent growth forecast for net sales in Q3 and Q4 of 2025. For each of the EU and the AU, I use a calibration exercise based on Q2 2025 earnings results relative to my original model's results for the same quarter to adjust the expected percentage point improvement in net sales between Q3 2024-->Q3 2025 and Q4 2024-->Q4 2025. I forecast no improvement in YoY percent growth of net sales in the EU unit for Q3 and Q4 2025. I forecast a 60 percentage point and 50 percentage point improvement in the YoY percent growth of net sales in the AU unit in Q3 and Q4 2025. These estimates are much higher in the AU unit relative to my forecast for Q2 2025, which reflects the substantial improvement in net sales for AU in Q2 2025.
* **Regional Cost of Sales:** My forecast for the regional cost of sales for Q2 2025 was highly accurate. I find that my Q2 2025 forecast for cost of sales as a percent of net sales (i.e., normalized for net sales) shows essentially no percent error relative to actual results for Q2 2025 in the US, EU, and AU units. The percent error in cost of sales prior to normalizing for net sales is greater at -6%, 0%, and -27% for the US, EU, and AU, respectively (negatives are underestimates). However, this is essentially entirely due to my underestimate of net sales, which showed a percent error of -7%, 0%, and -27% for the US, EU, and AU, respectively. Due to the high accuracy of the normalized cost of sales figures, I follow the same methodology for forecasting cost of sales in Q3 and Q4 2025 as I did in Q2 2025. This methodology assumes that the YoY percent change in normalized cost of sales is -10%, -1%, and 0% in the US, EU, and AU units, respectively, in Q3 and Q4 2025. For a fuller discussion of my methodology for cost of sales, please refer to the Appendix of my [Q2 2025 Forecast](https://github.com/justgmethings/GME_Earnings_Forecast/blob/main/forecasts/earnings_forecast_q2-2025.md).
* **Regional SG&A:** My forecast for SG&A for Q2 2025 was highly accurate in aggregate. My forecast for SG&A normalized for net sales was 22.4% in Q2 2025 versus 22.5% reported for the same quarter. However, there was some greater variation in the percent error for normalized SG&A within regional units, including a 1.5%, -26.1%, and 27.2% percent error in the US, EU, and AU units, respectively. I implement a calibration exercise using my model and the reported results for Q2 2025 to implement adjustments to forecasted SG&A in Q3 and Q4 of 2025. I assume the YoY percent growth in normalized SG&A will be 5%, 20%, and -30% in both Q3 and Q4 of 2025 in the US, EU, and AU units, respectively. The 5% growth for the US reflects an assumption of increased investments on new initiatives (e.g., PowerPacks) relative to last year. I assume that the 20% increase in the EU unit reflects efforts to sell the French operations (i.e., the remaining operations in the EU).
* **Estimate of Total Switch 2 Sales in US:** In my Q2 2025 forecast, I had projected 720k and 2.45 million units of Switch 2's would be sold in Q3 and Q4 2025, respectively. For my Q3 forecast, I increase my projection of Switch 2 units sold to 1 million units in Q3 and 3.06 million units in Q4, which both reflects updated data for [August](https://www.vgchartz.com/article/465961/2025-americas-sales-comparison-charts-through-august-switch-2-vs-ps5-vs-xbox-series-xs-vs-switch/) and [September](https://www.vgchartz.com/article/466068/2025-americas-sales-comparison-charts-through-september-switch-2-vs-ps5-vs-xbox-series-vs-switch/) and revised projections for the remainder of the year due to higher than expected reported sales in Q3 2025. I keep my assumption that 2.5 games and 1.5 accessories are sold for each Switch 2 console sold in FY 2025. I also continue to assume a weighted cost of Switch 2 consoles, games, and accessories of $450, $72.50, and $70, respectively.
* **Switch 2 Sales by GME:** To improve my model of Switch 2 sales, which relies on limited data, I conducted a calibration exercise between my model of Switch 2 sales and the aggregate results of Q2 2025 earnings. This exercise revealed that GME likely captured a greater amount of total sales than the 15% of U.S. Switch 2 sales that I assumed for Q2 2025. In Q3 and Q4 2025, I assume that GME will capture 20% of total Switch 2 sales in the US. This is still a conservative figure relative to [public data](https://www.theesa.com/u-s-consumer-spending-on-video-games-totaled-58-7-billion-in-2024/) showing that GME captured 26% of total U.S. hardware/accessory sales in FY 2024.[^1] In Q3 and Q4 2025, I make no changes to my assumption of 2.5% gross margins on consoles. In Q3 and Q4 2025, I increase the assumed gross margins on Switch 2 games and accessories each from 25% in Q2 to 33% as a result of my calibration exercise. I make no changes to the assumption from my Q2 forecast that SG&A related to Switch 2 sales is 2%. These components allow me to forecast total costs and total revenue from Switch 2 consoles, accessories, and software in the US. I continue to forecast AU and EU Switch 2 sales based on the relative population and GDP per capita of each of the countries represented in each of the regional business units relative to the US to get a “scaled” version of Switch 2 sales in each region outside the US. In total, I project $20.56 million and $190.36 million in total net income associated with sales of Switch 2 consoles, accessories, and software in Q3 2025 and FY 2025, respectively.
* **Interest Rates:** I assume that the company receives a 3.96% annual yield on its cash holdings in Q3 2025. Based on the prevailing market probabilities at the time of the forecast, I assume a 25 basis point interest rate cut at the Federal Reserve’s December meeting and no cut at the January meeting.
* **Interest Earnings:** I do not estimate the *additional* interest earnings accrued from future operating profits (e.g., interest earned in Q4 2025 from unspent operating profits in Q3 2025). This is simply done to improve the simplicity and tractability of my interest earnings model; however, it is a notable omission given my projections for operating income and, all else equal, will likely lead to my model underestimating interest income in FY 2025. I implicitly assume that there are no additional stock sales or convertible bonds that increase the company’s cash reserves. This assumption may further underestimate the company's future cash reserves due to the issuance of 1 warrant for each 10 shares held by shareholders. To the extent that these warrants are exercised in the remainder of FY 2025, this will further support GME's balance sheet since the $32 exercise price would be paid directly to the company.
* **BTC Earnings:** In my Q2 Forecast, I assumed a cost basis of $106.4k, which was nearly identical to the cost basis of $106.2 implicitly reported by the company in its Q2 earnings statement (i.e., I had assumed $501.1 million spent on BTC while the company reported $500 million spent). For my Q3 Forecast, I forecast an end-of-quarter value for BTC of $518 million, which corresponds with an estimate of $11.6 million in BTC losses for Q3 2025. While BTC is historically volatile, I project no change (gain or loss) in the value of the cryptocurrency in Q4, which reflects my uncertainty over its future direction. For those who disagree, this assumption is straightforward to adjust to reflect your preferred earnings estimate based on your own forecasted path for BTC. BTC earnings are now reflected in “Unrealized gain on digital assets”.
* **EU (French) Operations:** I assume that the remaining EU operation (i.e., France) is not sold until after end of the fiscal year, which is outside my forecast window. I base this on the updated guidance provied by GME in the Q3 2025 earnings statement, which reads "The sale of the operations in France is expected to close within the next 12 months."
* **Taxes:** I base my Q3 2025 forecast for income taxes on the ratio of reported income taxes to the sum of operating income (exclusive of impairments) and interest income reported in Q2 2025. I repeat this process for my forecast of Q4 2025 income taxes. I also add expected taxes for the PowerPacks program based on u/regionformal's estimates of those taxes.

[^1]: GME recorded $2.1 billion in gaming hardware sales in FY 2024. The [Entertainment Software Assocation](https://www.theesa.com/u-s-consumer-spending-on-video-games-totaled-58-7-billion-in-2024/) reported $8.1 billion in hardware/accessory sales. I assume that GME accessory sales are grouped into its hardware category. Therefore, GME hardware sales represented 25.9% of all U.S. gaming hardware sales.
