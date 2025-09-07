import pandas as pd
import numpy as np
import re

print("=== PHÂN TÍCH DỮ LIỆU BÊ TÔNG ===\n")

# 1. Đọc dữ liệu từ file
try:
    # Thử đọc file CSV trước
    file_path = "Concrete_Data_ThucHanh.xlsx - Sheet1.csv"
    df = pd.read_csv(file_path)
    print("✅ Đọc file CSV thành công!")
except FileNotFoundError:
    try:
        # Nếu không có file CSV, thử file Excel
        file_path = "Concrete_Data_ThucHanh.xlsx"
        df = pd.read_excel(file_path)
        print("✅ Đọc file Excel thành công!")
    except FileNotFoundError:
        print("❌ LỖI: Không tìm thấy file dữ liệu!")
        print("Vui lòng kiểm tra:")
        print("- File 'Concrete_Data_ThucHanh.xlsx - Sheet1.csv'")
        print("- Hoặc file 'Concrete_Data_ThucHanh.xlsx'")
        exit()

# Làm sạch tên cột
df.columns = df.columns.str.strip()

print(f"📊 Kích thước dữ liệu: {df.shape[0]} mẫu, {df.shape[1]} thuộc tính")
print(f"📋 Tên các cột: {list(df.columns)}")

print("\n" + "="*60)
print("1. KIỂM TRA GIÁ TRỊ THIẾU (MISSING VALUES)")
print("="*60)

missing_values = df.isnull().sum()
total_missing = missing_values.sum()

if total_missing > 0:
    print("⚠️ CÓ GIÁ TRỊ THIẾU:")
    for col, missing in missing_values.items():
        if missing > 0:
            percentage = (missing / len(df)) * 100
            print(f"   - {col}: {missing} giá trị ({percentage:.2f}%)")
else:
    print("✅ KHÔNG CÓ GIÁ TRỊ THIẾU")

print("\n" + "="*60)
print("2. KIỂM TRA DÒNG TRÙNG LẶP")
print("="*60)

duplicate_rows = df.duplicated()
num_duplicates = duplicate_rows.sum()

if num_duplicates > 0:
    print(f"⚠️ CÓ {num_duplicates} DÒNG TRÙNG LẶP:")
    duplicate_indices = df[duplicate_rows].index.tolist()
    print(f"   - Vị trí các dòng trùng: {duplicate_indices}")
    
    # Hiển thị một vài dòng trùng lặp
    if num_duplicates > 0:
        print("   - Ví dụ dòng trùng lặp:")
        print(df[duplicate_rows].head(3))
else:
    print("✅ KHÔNG CÓ DÒNG TRÙNG LẶP")

print("\n" + "="*60)
print("3. KIỂM TRA KÝ TỰ ĐẶC BIỆT")
print("="*60)

def check_special_characters(df):
    special_chars_found = {}
    
    for col in df.columns:
        if df[col].dtype == 'object':  # Chỉ kiểm tra cột text
            special_chars = []
            for idx, value in enumerate(df[col]):
                if pd.notna(value):
                    # Kiểm tra ký tự không phải chữ, số, khoảng trắng
                    special_pattern = re.findall(r'[^a-zA-Z0-9\s.]', str(value))
                    if special_pattern:
                        special_chars.append({
                            'row': idx,
                            'value': value,
                            'special_chars': list(set(special_pattern))
                        })
            
            if special_chars:
                special_chars_found[col] = special_chars
    
    return special_chars_found

special_chars_result = check_special_characters(df)

if special_chars_result:
    print("⚠️ CÓ KÝ TỰ ĐẶC BIỆT:")
    for col, issues in special_chars_result.items():
        print(f"   - Cột '{col}':")
        for issue in issues[:3]:  # Chỉ hiển thị 3 ví dụ đầu
            print(f"     * Dòng {issue['row']}: '{issue['value']}' - Ký tự: {issue['special_chars']}")
        if len(issues) > 3:
            print(f"     * ... và {len(issues)-3} trường hợp khác")
else:
    print("✅ KHÔNG CÓ KÝ TỰ ĐẶC BIỆT BẤT THƯỜNG")

print("\n" + "="*60)
print("4. TỔNG HỢP SỐ MẪU")
print("="*60)

print(f"📈 Tổng số mẫu ban đầu: {len(df)}")
print(f"📉 Số mẫu bị trùng lặp: {num_duplicates}")
print(f"📊 Số mẫu sau khi loại bỏ trùng lặp: {len(df) - num_duplicates}")

if num_duplicates > 0:
    df_clean = df.drop_duplicates()
    print("🧹 Đã tạo dataset sạch (loại bỏ trùng lặp)")
else:
    df_clean = df.copy()
    print("✅ Dataset đã sạch, không cần xử lý thêm")

print("\n" + "="*60)
print("5. XÁC ĐỊNH INPUT VÀ OUTPUT")
print("="*60)

# Giả định cột cuối là target (thường là cường độ bê tông)
features = df.columns[:-1].tolist()
target = df.columns[-1]

print(f"🎯 INPUT (Đầu vào) - {len(features)} thuộc tính:")
for i, feature in enumerate(features, 1):
    print(f"   {i:2d}. {feature}")

print(f"\n🎯 OUTPUT (Đầu ra):")
print(f"   - {target}")

print("\n" + "="*60)
print("6. MỤC ĐÍCH DỰ ĐOÁN")
print("="*60)

print("🏗️ MỤC ĐÍCH CỦA MÔ HÌNH:")
print("   • Dự đoán CƯỜNG ĐỘ BÊ TÔNG dựa trên thành phần nguyên liệu")
print("   • Ứng dụng:")
print("     - Tối ưu hóa công thức bê tông")
print("     - Kiểm soát chất lượng trong sản xuất")
print("     - Tiết kiệm chi phí nguyên liệu")
print("     - Đảm bảo độ bền công trình")

print("\n" + "="*60)
print("7. THỐNG KÊ MÔ TẢ")
print("="*60)

print("📊 THỐNG KÊ CƠ BẢN:")
print(df.describe().round(2))

print("\n🎯 PHÂN TÍCH TARGET:")
if pd.api.types.is_numeric_dtype(df[target]):
    print(f"   - Giá trị nhỏ nhất: {df[target].min():.2f}")
    print(f"   - Giá trị lớn nhất: {df[target].max():.2f}")
    print(f"   - Giá trị trung bình: {df[target].mean():.2f}")
    print(f"   - Độ lệch chuẩn: {df[target].std():.2f}")

print("\n✅ HOÀN THÀNH PHÂN TÍCH DỮ LIỆU!")
from pathlib import Path
import pandas as pd

# Đường dẫn đầy đủ
file_path = Path(r'C:\Users\Admin\OneDrive\Desktop\python2\Concrete_Data_ThucHanh.xlsx')
df = pd.read_excel(file_path)