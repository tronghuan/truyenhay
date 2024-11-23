import requests
import json
import re
from bs4 import BeautifulSoup

# # URL của trang chứa danh sách các bộ truyện
# url = "https://truyenfull.vn/the-loai/tien-hiep/"

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Giả sử các bộ truyện được chứa trong các thẻ <div> với class "truyen"
# truyen_list = soup.find_all('div', class_='col-xs-7')

# for truyen in truyen_list:
#     title = truyen.find('h3').text  # Giả sử tiêu đề truyện nằm trong thẻ <h2>
#     link = truyen.find('a')['href']  # Giả sử link truyện nằm trong thẻ <a>
#     print(f"Title: {title}, Link: {link}")

# Hàm để lưu JSON vào file
def save_json(data, filename='tien_nghich.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Tạo mới chương
def add_chuong(data, so_chuong, so_trang, tieu_de_chuong=None, link_chuong=None):
    chuong = {
        "so_chuong": so_chuong,
        "trang": so_trang,
        "tieu_de_chuong": tieu_de_chuong,
        "link_chuong": link_chuong
    }
    data["danh_sach_chuong"].append(chuong)
    # print(f"Chương {so_chuong}: {tieu_de_chuong} {link_chuong} đã được thêm thành công.")

# Cập nhật chương
def update_chuong(data, so_chuong, so_trang, tieu_de_chuong=None, link_chuong=None):
    for chuong in data["danh_sach_chuong"]:
        if chuong["so_chuong"] == so_chuong:
            if so_trang:
                chuong["trang"] = so_trang
            if tieu_de_chuong:
                chuong["tieu_de_chuong"] = tieu_de_chuong
            if link_chuong:
                chuong["link_chuong"] = link_chuong
            print(f"Chương {so_chuong}: {tieu_de_chuong} đã được cập nhật.")
            return
    # print(f"Không tìm thấy Chương {so_chuong}: {tieu_de_chuong}.")

# Xóa chương
def delete_chuong(data, so_chuong):
    for i, chuong in enumerate(data["danh_sach_chuong"]):
        if chuong["so_chuong"] == so_chuong:
            del data["chuong"][i]
            # print(f"Chương {so_chuong} đã được xóa.")
            return
    # print(f"Không tìm thấy chương {so_chuong}.")

# Lấy tổng số trang của danh sách chương của truyện
def get_tong_so_trang(chapter_title):
    tong_so_trang = 1
    if 'Tiên Nghịch - Trang' in chapter_title:
        match = re.search(r"Trang (\d+)", chapter_title)
        if match:
            chapter_number = int(match.group(1))
            if chapter_number > tong_so_trang:
                tong_so_trang = chapter_number
            # print("chapter_number: ", chapter_number)
            # print("tong_so_trang: ", tong_so_trang)
    return tong_so_trang
    


def get_truyen_details(truyen_url):
    response = requests.get(truyen_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Giả sử các thông tin cần thiết được chứa trong các thẻ cụ thể
    title = soup.find('h1').text  # Tiêu đề
    # Lấy thông tin tác giả
    tac_gia = soup.find('a', itemprop='author').text
    # Lấy thông tin thể loại
    the_loai = [genre.text for genre in soup.find_all('a', itemprop='genre')]
    # Lấy thông tin trạng thái
    trang_thai = soup.find('span', class_='text-success').text
    # so_chuong = soup.find('div', class_='so-chuong').text  # Số chương

    # Lấy danh sách các chương
    chapter_list = soup.find_all('a', href=True, title=True)

    chapters = []
    so_trang = []
    tong_so_trang = 1
    for chapter in chapter_list:
        chapter_title = chapter['title']
        chapter_link = chapter['href']
        if title in chapter_title and 'tien-nghich' in chapter_link and 'chuong-' in chapter_link:
            chapters.append({'title': chapter_title, 'link': chapter_link})
        if 'Tiên Nghịch - Trang' in chapter_title:
            so_trang.append({'title': chapter_title, 'link': chapter_link})
    
    print("Số trang: ", so_trang)

    # Dữ liệu mẫu ban đầu
    # data_truyen = {
    #     "ten_truyen": "Tiên Nghịch",
    #     "tac_gia": "Tiêu Đỉnh",
    #     "the_loai": "Tiên Hiệp",
    #     "danh_sach_chuong": [
    #         {
    #             "so_chuong": 1,
    #             "trang":1,
    #             "tieu_de_chuong": 1,
    #             "link_chuong": "http://abv.com",
    #         },
    #         {
    #             "so_chuong": 1,
    #             "trang":1,
    #             "tieu_de_chuong": 1,
    #             "link_chuong": "http://abv.com",
    #         }
    #     ]
    # }

    # Các biến chứa thông tin cần truyền vào JSON
    ten_truyen = "Tiên Nghịch"
    tac_gia = "Tiêu Đỉnh"
    the_loai = "Tiên Hiệp"
    danh_sach_chuong = []

    # Tạo dictionary từ các biến
    data_truyen = {
        "ten_truyen": ten_truyen,
        "tac_gia": tac_gia,
        "the_loai": the_loai,
        "tong_so_trang": tong_so_trang,
        "danh_sach_chuong": danh_sach_chuong
    }

    # Tính tổng số trang
    for trang in so_trang:
        tong_so_trang = get_tong_so_trang(trang['title'])
    
    print("Tổng số trang: ", tong_so_trang)
    # In danh sách các chương
    tong_so_trang = 2
    for trang in range(tong_so_trang):
        i = 1
        for chapter in chapters:
            add_chuong(data_truyen, i, trang, chapter["title"], chapter["link"])
            i = i + 1

    # Lưu lại JSON sau khi thực hiện các thao tác
    save_json(data_truyen)

    return data_truyen

def get_chuong_content(chuong_url):
    response = requests.get(chuong_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(f"Đang lấy nội dung chương từ {chuong_url}...")
    # print(soup)
    # print("Lấy nội dung chương thành công!!!")
    
    # Lấy nội dung của đoạn div với id là "chapter-c"
    chapter_content = soup.find('div', {'id': 'chapter-c'}).get_text(separator='\n', strip=True)
    return chapter_content

def insert_chuong(content):
    import sqlite3

    # Kết nối đến cơ sở dữ liệu (sẽ tạo ra cơ sở dữ liệu nếu nó không tồn tại)
    conn = sqlite3.connect('tien_nghich.db')

    # Tạo con trỏ để thực hiện các truy vấn
    cursor = conn.cursor()

    # Chèn một hàng dữ liệu
    cursor.execute('''
    INSERT INTO tien_nghich (content) VALUES (?)
    ''', (content,))

    # # Chèn nhiều hàng dữ liệu
    # contents = [
    #     (content),
    #     (content)
    # ]
    # cursor.executemany('''
    # INSERT INTO tien_nghich (content) VALUES (?)
    # ''', contents)

    # Lưu các thay đổi
    conn.commit()
    print("Lưu nội dung chương thành công!!!")

    # Đóng kết nối cơ sở dữ liệu
    conn.close()

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

def create_link_truyen(url, ten_truyen):
    return url + "/" + ten_truyen

def get_chapter_contents(data_truyen):
    i = 1
    for chuong in data_truyen["danh_sach_chuong"]:
        content = get_chuong_content(chuong['link_chuong'])
        content_template =  f"""
            <!-- Nội dung trang truyện -->
            <div class="row mt-4">

                <div class="col-12 content">
                    <h1 class="text-center">Tên Truyện</h1>
                    {content.replace('\n', '<br /><br />')}
                </div>
            </div>
            """

        # Dùng BeautifulSoup để format HTML
        soup = BeautifulSoup(content_template, "html.parser")
        formatted_content = soup.prettify()
        ten_chuong = "chuong-" + str(i) + ".html"
        # Lưu nội dung vào tệp HTML
        with open(ten_chuong, "w", encoding="utf-8") as file:
            file.write(formatted_content)
        i = i + 1

main("https://truyenfull.io", "tien-nghich")

# get_truyen_details("https://truyenfull.io/tien-nghich/")


# Ví dụ: Lấy nội dung của một chương cụ thể
# chuong_url = "https://truyenfull.io/tien-nghich/chuong-1/"
# content = get_chuong_content(chuong_url)
# insert_chuong(content)
# print(content)


# content_template = f"""
# <!-- Nội dung trang truyện -->
# <div class="row mt-4">

#     <div class="col-12 content">
#         <h1 class="text-center">Tên Truyện</h1>
#         {content.replace('\n', '<br /><br />')}
#     </div>
# </div>
# """

# # Lưu nội dung vào tệp HTML
# with open("chuong-1.html", "w", encoding="utf-8") as file:
#     file.write(content_template)

# print("Đã tạo tệp HTML thành công!")
