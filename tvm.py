def tvm_monthly_installments(principal, rate, years):
    r = rate / 100 / 12  
    n = years * 12  
    monthly_payment = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)

    print(f"{'Month':<6} {'Discounted EMI Value':<20}")
    print("=" * 30)

    for month in range(1, n + 1):
        discounted_emi = monthly_payment / ((1 + r) ** month)  
        print(f"{month:<6} {discounted_emi:<20.2f}")

principal = 100000  
rate = 12  
years = 2  

tvm_monthly_installments(principal, rate, years)
