# Simple Quantitative Algorithm for Wharton Global Investment Competition
[wharton logo]: https://github.com/nalm1223/wharton-quant-algo-2026/blob/main/images/wharton%20logo.avif
[global competition logo]: https://github.com/nalm1223/wharton-quant-algo-2026/blob/main/images/global%20competition%20logo.avif

![alt text][wharton logo]

## Table Of Contents
- [Initial Algorithm Objectives](#initial-algorithm-objectives)
- [Rationale](#rationale)
- [Assumptions](#assumptions)
- [Results](#results)
  - [Competition Outcomes](#competition-outcomes)
  - [Following Competition](#following-competition)
- [Further Research](#further-research)
- [Sources](#sources)

## Initial Algorithm Objectives
The case study (Laura Gao) objectives include:
- The creation of a portfolio with an initial investment of $300,000
- An additional investment of $150,000 one year after the brokerage account is opened
- A $50,000 annual drawdown six years after the account opens

Stock selection was dictated by fundamental research done by our team, so the algorithm would need to
- Find the amount of money to put into each chosen stock to ensure a balance of risk and return for initial investments
- Create a distribution for possible returns for the portfolio
- Make the best allocations/deallocations that fit Laura's goals

## Rationale

## Assumptions
- Projected return outcomes will follow a normal distribution $\mathcal{N}(\mu,\sigma^2)$, where its mean ($\mu$) is equal to the portfolio's annualized return, and its variance ($\sigma^2$) is the standard deviation of the ticker or portfolio squared
- The standard deviation and annualized return for each ticker (stock) remains constant over the course of the account's position in the market

## Results
### Competition Outcomes
Due to the unfortunate circumstances, we were not able to continue development of the algorithm within the competition due to a disqualification (a deliverable was not turned in at the deadline). Despite this, many of the initial objectives of our algorithm were able to be completed.

Firstly, sharpe portfolio optimization was able to be implemented, and from that initial balances of assets could take place. Given our initial budget and trades made in StockTrak, our algorithm was able to find the allocation weighting strategy best fit to both a high sharpe ratio and our boundary conditions discussed in our Rationale.
```
Initial Weights: 
[0.10541159 0.10461853 0.10554775 0.22596566 0.07855724 0.10468204
 0.1180922  0.157125  ]
Initial Return: 0.10941451809666095, Initial STD: 0.14239456031122955
Initial Sharpe Ratio: -0.5573860696436768

Optimized Weights: 
[0.27122521 0.05012215 0.09220157 0.05010336 0.38629033 0.04987927
 0.05001688 0.05016121]
Optimized Return: 0.16123408497635527, Optimized STD: 0.170838810618703
Optimized Sharpe Ratio: -0.7901960358718285
```
From these optimized allocation weights, allocations to each ticker can be made, rounding each weight to the nearest whole share of each stock:
| Symbol | Number of Shares |
| ----   |       :---:      |
| GLD    | 216              |
| INTF   | 367              |
| PG     | 165              |
| SCHD   | 423              |
| SMH    | 258              |
| VNQ    | 155              |
| VPU    | 80               |
| VTV    | 67               |



### Following Competition

## Further Research
Through future projects, the usage of algorithmic trading 

## Sources
