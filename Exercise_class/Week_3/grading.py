score = float(input('Type your score: '))

if score >= 90:
    print(f'Grade A with score {score}')
else:
    if score >= 80:
        print(f'Grade B with score {score}')
    else:
        if score >= 70:
            print(f'Grade C with score {score}')
        else:
            if score >= 60:
                print(f'Grade D with score {score}')
            else:
                if score >= 50:
                    print(f'Grade E with score {score}')
                else:
                    print(f'Grade F with score {score}')