# Thực hiện crawl truyện lại từ tất cả website truyện
def main():
    print("Crawl truyện từ tất cả website truyện...")
    # Step 1: Lấy danh sách website truyện(danh sách được đặt trong file txt/csv)

    # Step 2: Lấy danh sách truyện từ mỗi website truyện

    # Step 3: Lấy danh sách chương từ mỗi truyện

    # Step 4: Lấy nội dung từng chương

    # Step 5: Lưu nội dung chường vào file html

    # Step 6: Copy file html sang thư mục tương ứng

# Thực hiện crawl truyện lại từ một website truyện cụ thể
def main(url):
    print(f"Crawl truyện từ website truyện {url}...")
    # Step 1: Lấy danh sách truyện từ url truyền vào

    # Step 2: Lấy danh sách chương từ mỗi truyện

    # Step 3: Lấy nội dung từng chương

    # Step 4: Lưu nội dung chường vào file html

    # Step 5: Copy file html sang thư mục tương ứng


# Thực hiện crawl truyện cụ thể từ một website truyện cụ thể
def main(url, ten_truyen):
    # Step 1: Lấy danh sách chương từ url và ten_truyen truyền vào
    link_truyen = create_link_truyen(url, ten_truyen)
    data_truyen = get_truyen_details(link_truyen)


    # Step 2: Lấy nội dung từng chương
    get_chapter_contents(data_truyen)

    # Step 3: Lưu nội dung chường vào file html

    # Step 4: Copy file html sang thư mục tương ứng