def function_x():
    pass
    Ellipsis
    ...

def read_sales():
    sales = [1200, 800, 950, 1100]
    return sales

def summarize_sales(sales):
    total = sum(sales)
    avg = total / len(sales)
    return total, avg

def print_report(total, avg):
    print(f"Total = {total}, Average = {avg:.2f}")

def main():
    sales = read_sales()
    total, avg = summarize_sales(sales)
    print_report(total, avg)
main()