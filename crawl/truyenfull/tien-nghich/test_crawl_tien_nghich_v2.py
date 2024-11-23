import unittest
from unittest.mock import patch, MagicMock, mock_open
from crawl_tien_nghich_v2 import main, create_link_truyen, get_tong_so_trang, get_danh_sach_chuong, get_chapter_contents

class TestCrawlTienNghich(unittest.TestCase):

    @patch('crawl_tien_nghich_v2.requests.get')
    def test_get_tong_so_trang(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <ul class="pagination">
                <li><a title="Tiên Nghịch - Trang 1">1</a></li>
                <li><a title="Tiên Nghịch - Trang 2">2</a></li>
                <li><a title="Tiên Nghịch - Trang 3">3</a></li>
                <li><a title="Tiên Nghịch - Trang tùy chọn">Chọn trang</a></li>
            </ul>
        </html>
        '''
        mock_get.return_value = mock_response

        link_truyen = "http://example.com/truyen/tien-nghich"
        tong_so_trang = get_tong_so_trang(link_truyen)
        self.assertEqual(tong_so_trang, 3)

    @patch('crawl_tien_nghich_v2.requests.get')
    def test_get_danh_sach_chuong(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <ul class="list-chapter">
                <li><a href="http://example.com/chuong-1" title="Chương 1">Chương 1</a></li>
                <li><a href="http://example.com/chuong-2" title="Chương 2">Chương 2</a></li>
            </ul>
            <ul class="list-chapter">
                <li><a href="http://example.com/chuong-3" title="Chương 3">Chương 3</a></li>
                <li><a href="http://example.com/chuong-4" title="Chương 4">Chương 4</a></li>
            </ul>
        </html>
        '''
        mock_get.return_value = mock_response

        link_truyen = "http://example.com/truyen/tien-nghich"
        tong_so_trang = 1
        danh_sach_chuong = get_danh_sach_chuong(link_truyen, tong_so_trang)
        expected = [
            {'link_chuong': 'http://example.com/chuong-1', 'ten_chuong': 'Chương 1'},
            {'link_chuong': 'http://example.com/chuong-2', 'ten_chuong': 'Chương 2'},
            {'link_chuong': 'http://example.com/chuong-3', 'ten_chuong': 'Chương 3'},
            {'link_chuong': 'http://example.com/chuong-4', 'ten_chuong': 'Chương 4'}
        ]
        self.assertEqual(danh_sach_chuong, expected)

    def test_create_link_truyen(self):
        url = "http://example.com"
        ten_truyen = "tien-nghich"
        expected = "http://example.com/tien-nghich"
        self.assertEqual(create_link_truyen(url, ten_truyen), expected)

    @patch('crawl_tien_nghich_v2.requests.get')
    @patch('crawl_tien_nghich_v2.open', new_callable=mock_open)
    def test_get_chapter_contents(self, mock_open, mock_get):
        # Mock response for requests.get
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <h2>
                <a class="chapter-title" href="https://truyenfull.io/tien-nghich/chuong-1/" title="Tiên Nghịch - Chương 1: Ly hương">
                <span class="chapter-text">
                Chương
                </span>
                </span>
                1: Ly hương
                </a>
            </h2>
            <div class="chapter-c" id="chapter-c" itemprop="articleBody">
                Thiết Trụ ngồi ở bên con đường nhỏ trong thôn, vẻ mặt ngẩn ngơ nhìn bầu trời xanh thẳm, Thiết Trụ vốn không phải là tên thật của hắn, mà là từ bé bởi vì thân thể gầy yếu, phụ thân sợ nuôi không được, vì thế dựa theo tập tục mà gọi tên mụ.
                <br/>
                <br/>
                Hắn vốn tên là Vương Lâm, họ Vương ở trong vài cái thôn xóm xung quanh xem như danh gia, tổ tiên xuất thân thợ mộc, nhất là ở thị trấn, gia tộc họ Vương cũng coi như rất có danh tiếng, có được mấy cửa hiệu chuyên môn bán sản phẩm gỗ.
                <br/>
                <br/>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response

        # Mock data_truyen
        data_truyen = [
            {'link_chuong': 'http://example.com/chuong-1', 'ten_chuong': 'Tiên Nghịch - Chương 1: Ly hương'}
        ]

        # Call the function
        get_chapter_contents(data_truyen)

        # Check if requests.get was called with the correct URL
        mock_get.assert_called_with('http://example.com/chuong-1')

        # Check if the file was opened with the correct path and mode
        mock_open.assert_called_with('danh-sach-chuong/chuong-1.html', 'w', encoding='utf-8')

        # Check if the correct content was written to the file
        handle = mock_open()
        handle.write.assert_called_once()
        written_content = handle.write.call_args[0][0]

        self.assertIn('<h1 class="text-center">Tiên Nghịch - Chương 1: Ly hương</h1>', written_content)
        self.assertIn('Thiết Trụ ngồi ở bên con đường nhỏ trong thôn, vẻ mặt ngẩn ngơ nhìn bầu trời xanh thẳm, Thiết Trụ vốn không phải là tên thật của hắn, mà là từ bé bởi vì thân thể gầy yếu, phụ thân sợ nuôi không được, vì thế dựa theo tập tục mà gọi tên mụ.<br /><br />', written_content)
        self.assertIn('Hắn vốn tên là Vương Lâm, họ Vương ở trong vài cái thôn xóm xung quanh xem như danh gia, tổ tiên xuất thân thợ mộc, nhất là ở thị trấn, gia tộc họ Vương cũng coi như rất có danh tiếng, có được mấy cửa hiệu chuyên môn bán sản phẩm gỗ.<br /><br />', written_content)

if __name__ == '__main__':
    unittest.main()