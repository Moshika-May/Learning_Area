def count_duplicates(list_int):
    seen = set()       # สร้าง set ว่างๆ เอาไว้จำตัวเลขที่เคยเจอแล้ว
    duplicates = 0     # ตัวนับจำนวนตัวซ้ำ
    
    for num in list_int:
        if num in seen:
            duplicates += 1   # ถ้าเคยเจอแล้ว แปลว่าเป็นตัวซ้ำ ให้นับเพิ่ม
        else:
            seen.add(num)     # ถ้ายังไม่เคยเจอ ให้จำใส่ set ไว้
            
    return duplicates

def main():
    a = [2, 4, 6, 8, 10, 12, -2, -4]
    print(count_duplicates(a))

if __name__ == "__main__":
    main()