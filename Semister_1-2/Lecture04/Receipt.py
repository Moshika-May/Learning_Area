def main():
    sub_total = 38 + 40 + 30
    tax = (sub_total * .08)
    tip = (sub_total * .15)
    total = (sub_total + tax + tip)

    print("Subtotal:")              # Compute total 
    print(sub_total)                # owed, assuming
    print("Tax:")                   # 8% tax and
    print(tax)                      # 15% tip
    print("Tip:")
    print(tip)
    print("Total:")
    print(total)

if __name__ == "__main__":
    main()