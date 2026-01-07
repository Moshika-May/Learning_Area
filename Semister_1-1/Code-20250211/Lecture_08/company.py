def print_company_data(company):
    """Prints the company data in a table format using nested loops."""
    for department, employees in company.items():
        print(f"\nDepartment: {department}")
        print(f"{'Name':<10} {'Age':<5} {'Position':<20} {'Email':<25}")
        for name, details in employees.items():
            print(f"{name:<10}", end=" ")
            for key, value in details.items():
                if key == 'age':
                    print(f"{value:<5}", end=" ")
                elif key == 'position':
                    print(f"{value:<20}", end=" ")
                elif key == 'email':
                    print(f"{value:<25}", end=" ")
            print()  # for newline
            
def main():
    company = {
        'Engineering': {
            'Alice': {'age': 29, 'position': 'Software Engineer', 'email': 'alice@company.com'},
            'Bob': {'age': 34, 'position': 'DevOps Engineer', 'email': 'bob@company.com'}
        },
        'HR': {
            'Charlie': {'age': 40, 'position': 'HR Manager', 'email': 'charlie@company.com'},
            'Daisy': {'age': 28, 'position': 'Recruiter', 'email': 'daisy@company.com'}
        },
        'Marketing': {
            'Eve': {'age': 35, 'position': 'Marketing Specialist', 'email': 'eve@company.com'},
            'Frank': {'age': 31, 'position': 'SEO Expert', 'email': 'frank@company.com'}
        }
    }    
    print_company_data(company)
    
main()
