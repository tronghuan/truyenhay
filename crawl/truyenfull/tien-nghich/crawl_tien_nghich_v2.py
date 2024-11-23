# Import thư viện cần thiết
import requests
import json
import re
import os
from bs4 import BeautifulSoup

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
    # Step 1: Lấy tổng số trang của danh sách chương của truyện
    link_truyen = create_link_truyen(url, ten_truyen)

    # Lấy tổng số trang của danh sách chương
    tong_so_trang = get_tong_so_trang(link_truyen)

    # Step 2: Lấy danh sách chương từ url và ten_truyen truyền vào
    data_truyen = get_danh_sach_chuong(link_truyen, tong_so_trang)


    # Step 2: Lấy nội dung từng chương
    get_chapter_contents(data_truyen)

    # Step 3: Lưu nội dung chường vào file html

    # Step 4: Copy file html sang thư mục tương ứng

# Tạo link truyện
def create_link_truyen(url, ten_truyen):
    return url + "/" + ten_truyen

# Lấy tổng số trang của danh sách chương
def get_tong_so_trang(link_truyen):
    response = requests.get(link_truyen)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('ul', class_='pagination').find_all('li')[-2].find('a').get('title')

    tong_so_trang = 0
    print(f"Title: {title}")
    if 'Tiên Nghịch - Trang' in title:
        match = re.search(r"Trang (\d+)", title)
        if match:
            tong_so_trang = int(match.group(1))
    print(f"Tổng số trang: {tong_so_trang}")
    return tong_so_trang

def get_danh_sach_chuong(link_truyen, tong_so_trang):
    danh_sach_chuong = []
    print(f"Tổng số trang: {tong_so_trang}")
    tong_so_trang = 1 # TODO: Chỉ lấy 1 trang để test
    for trang in range(1, tong_so_trang + 1):
        link_trang = f"{link_truyen}/trang-{trang}/#list-chapter"
        response = requests.get(link_trang)
        soup = BeautifulSoup(response.text, 'html.parser')

        # NOTE: Do danh sách chương trong 1 trang được chia thành nhiều class list-chapter nên cần lấy tất cả các class list-chapter
        # list_chapter = soup.find('ul', class_='list-chapter').find_all('li')
        # print(f"List chapter: {list_chapter}")
        # for chapter in list_chapter:
        #     link_chapter = chapter.find('a').get('href')
        #     ten_chapter = chapter.find('a').get('title')
        #     danh_sach_chuong.append({
        #         'link_chuong': link_chapter,
        #         'ten_chuong': ten_chapter
        #     })

        # Lấy tất cả các danh sách chương trong class list-chapter
        list_chapters = soup.find_all('ul', class_='list-chapter')
        
        for list_chapter in list_chapters:
            chapters = list_chapter.find_all('li')
            for chapter in chapters:
                link_chapter = chapter.find('a').get('href')
                ten_chapter = chapter.find('a').get('title')
                danh_sach_chuong.append({
                    'link_chuong': link_chapter,
                    'ten_chuong': ten_chapter
                })
    # print(f"Danh sách chương: {danh_sach_chuong}")
    save_json(danh_sach_chuong, 'tien_nghich.json')
    return danh_sach_chuong

# Hàm để lưu JSON vào file
def save_json(data, filename='tien_nghich.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Lấy nội dung từng chương
def get_chapter_contents(data_truyen):
    i = 1
    for chuong in data_truyen:
        link_chuong = chuong['link_chuong']
        response = requests.get(link_chuong)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"soup: {soup.prettify()}")
        content = soup.find('div', class_='chapter-c').get_text(separator='\n', strip=True)
        # print(f"Nội dung chương {chuong['ten_chuong']}: {content}")
        content_template =  f"""
            <!-- Nội dung trang truyện -->
            <div class="row mt-4">

                <div class="col-12 content">
                    <h1 class="text-center">{chuong['ten_chuong']}</h1>
                    {content.replace('\n', '<br /><br />')}
                </div>
            </div>
            """

        # Dùng BeautifulSoup để format HTML
        soup = BeautifulSoup(content_template, "html.parser")
        formatted_content = soup.prettify()
        
        thu_muc = "danh-sach-chuong"
        ten_chuong = "chuong-" + str(i) + ".html"
        path_chuong = thu_muc + "/" + ten_chuong
        # Lưu nội dung vào tệp HTML
        with open(path_chuong, "w", encoding="utf-8") as file:
            file.write(formatted_content)
        i = i + 1
        break # TODO: Chỉ lấy 1 chương để test
# Run main function
if __name__ == "__main__":
    url = "https://truyenfull.io"
    ten_truyen = "tien-nghich"
    main(url, ten_truyen)