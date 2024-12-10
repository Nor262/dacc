import os  # Thư viện chuẩn của Python để tương tác với hệ điều hành
import sys  # Thư viện chuẩn của Python để làm việc với các tham số và hàm hệ thống
import math  # Thư viện chuẩn của Python cung cấp các hàm toán học
import random  # Thư viện chuẩn của Python để tạo ra các số ngẫu nhiên
import pygame  # Thư viện Pygame để phát triển trò chơi
import time

# Import các hàm và lớp từ các module tùy chỉnh
from scripts.utils import load, load_images, Animation  # Tải hình ảnh và hoạt ảnh
from scripts.entities import PhysicsEntity, Player, Enemy  # Các thực thể trong trò chơi như người chơi và kẻ thù
from scripts.tilemap import Tilemap  # Bản đồ ô vuông của trò chơi

class Game:
    def __init__(self):
        pygame.init()  # Khởi tạo tất cả các mô-đun của Pygame
        pygame.display.set_caption('Man In Red')  # Đặt tiêu đề cho cửa sổ game
        self.screen = pygame.display.set_mode((640, 480))  # Tạo cửa sổ game với kích thước 640x480
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)  # Tạo bề mặt hiển thị với kích thước 320x240 và hỗ trợ độ trong suốt
        self.display_1 = pygame.Surface((320, 240))  # Tạo bề mặt hiển thị thứ hai với kích thước 320x240
        self.st=time.time()
        self.clock = pygame.time.Clock()  # Tạo đồng hồ để quản lý thời gian
        
        self.movement = [False, False]  # Biến để theo dõi trạng thái di chuyển (trái/phải)
        
        self.assets = {  # Tải các tài nguyên hình ảnh và hoạt ảnh
            'decor': load_images('tiles/decor'),  # Tải hình ảnh trang trí
            'grass': load_images('tiles/grass'),  # Tải hình ảnh cỏ
            'large_decor': load_images('tiles/large_decor'),  # Tải hình ảnh trang trí lớn
            'stone': load_images('tiles/stone'),  # Tải hình ảnh đá
            'player': load('entities/player.png'),  # Tải hình ảnh người chơi
            'background': load('background.png'),  # Tải hình ảnh nền
            'enemy/idle': Animation(load_images('entities/enemy/idle'), anh=1),  # Tải ảnh kẻ thù đứng yên
            'enemy/run': Animation(load_images('entities/enemy/run'), anh=1),  # Tải ảnh kẻ thù chạy
            'player/idle': Animation(load_images('entities/player/idle'), anh=6),  # Tải hoạt ảnh người chơi đứng yên
            'player/run': Animation(load_images('entities/player/run'), anh=4),  # Tải hoạt ảnh người chơi chạy
            'player/jump': Animation(load_images('entities/player/jump')),  # Tải hoạt ảnh người chơi nhảy
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),  # Tải hoạt ảnh người chơi trượt tường
            'gun': load('gun.png'),  # Tải hình ảnh súng
            'projectile': load('projectile.png'),  # Tải hình ảnh đạn
        }
        
        self.sfx = {  # Tải các hiệu ứng âm thanh
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),  # Tải âm thanh nhảy
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),  # Tải âm thanh lao
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),  # Tải âm thanh va chạm
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),  # Tải âm thanh bắn
        }

        self.sfx['shoot'].set_volume(0.3)  # Đặt âm lượng cho âm thanh bắn
        self.sfx['hit'].set_volume(0.8)  # Đặt âm lượng cho âm thanh va chạm
        self.sfx['dash'].set_volume(0.2)  # Đặt âm lượng cho âm thanh lao
        self.sfx['jump'].set_volume(0.3)  # Đặt âm lượng cho âm thanh nhảy
        self.player = Player(self, (50, 50), (8, 15))  # Tạo đối tượng người chơi với vị trí và kích thước ban đầu
        self.tilemap = Tilemap(self)  # Tạo đối tượng bản đồ ô vuông với kích thước ô là 16
        self.level = 0  # Đặt bản đồ ban đầu là 0
        self.load_level(self.level)  # Tải bản đồ ban đầu
        self.screenshake=0
        self.phadao=False
        
    def load_level(self, map_id):
        if self.level>3:
            with open("bangxephang.txt", "a", encoding="utf-8") as file:
                file.write(f"{time.time()-self.st}s\n")  # Thời gian mặc định là 0 giây
            self.tilemap.load('data/maps/win.json')
            self.phadao=True         
        else:
            self.tilemap.load('data/maps/' + str(map_id) + '.json')  # Tải bản đồ từ file JSON dựa trên map_id

        self.enemies = []  # Danh sách để lưu các kẻ thù
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):  # Lấy các vị trí sinh ra từ bản đồ
            if spawner['variant'] == 0:  # Nếu là vị trí sinh ra người chơi
                self.player.pos = spawner['pos']  # Đặt vị trí người chơi
                self.player.air_time = 0  # Đặt thời gian trên không của người chơi về 0
            else:  # Nếu là vị trí sinh ra kẻ thù
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))  # Thêm kẻ thù vào danh sách
            
        self.projectiles = []  # Danh sách để lưu các viên đạn
        
        self.scroll = [0, 0]
        self.dead = 0  
        
    def run(self):
        # Tải file nhạc 'music.wav' từ thư mục 'data'
        pygame.mixer.music.load('data/nhac dang xinh.wav')
        # Đặt âm lượng của nhạc nền
        pygame.mixer.music.set_volume(0.1)
        # Phát nhạc nền lặp lại vô hạn
        pygame.mixer.music.play(-1)
        
        while True:
            # Làm sạch màn hình hiển thị
            self.display.fill((0, 0, 0, 0))
            # Vẽ nền
            self.display_1.blit(self.assets['background'], (0, 0))
            
            # Kiểm tra nếu không còn kẻ thù
            if not len(self.enemies) and self.level!=4:
                self.level += 1
                self.load_level(self.level)

            # Kiểm tra nếu người chơi đã chết
            if self.dead:
                self.dead += 1
                # Nếu người chơi đã chết trong hơn 40 khung hình, tải lại bản đồ hiện tại
                if self.dead > 40:
                    if self.phadao==False:
                        self.level=0 
                    self.load_level(self.level)
            
            # Cập nhật vị trí cuộn màn hình theo vị trí của người chơi
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, offset=render_scroll)  # Vẽ bản đồ lên bề mặt hiển thị
            
            # Cập nhật và vẽ kẻ thù
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))  # Cập nhật trạng thái kẻ thù
                enemy.render(self.display, offset=render_scroll)  # Vẽ kẻ thù lên bề mặt hiển thị
                if kill:  # Nếu kẻ thù bị tiêu diệt
                    self.enemies.remove(enemy)  # Xóa kẻ thù khỏi danh sách

            if not self.dead:  # Nếu người chơi chưa chết
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))  # Cập nhật trạng thái người chơi
                self.player.render(self.display, offset=render_scroll)  # Vẽ người chơi lên bề mặt hiển thị

            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]  # Cập nhật vị trí đạn theo hướng di chuyển
                projectile[2] += 1  # Tăng giá trị bộ đếm thời gian của đạn
                img = self.assets['projectile']  # Lấy hình ảnh đạn
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))  # Vẽ đạn lên bề mặt hiển thị
                if self.tilemap.solid_check(projectile[0]):  # Kiểm tra va chạm với bản đồ
                    self.projectiles.remove(projectile)  # Xóa đạn nếu va chạm
                elif projectile[2] > 360:  # Xóa đạn nếu tồn tại quá lâu
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:  # Kiểm tra va chạm với người chơi
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1  # Tăng giá trị chết của người chơi
                        self.sfx['hit'].play()  # Phát âm thanh va chạm

            # Tạo hiệu ứng bóng đổ cho các đối tượng
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_1.blit(display_sillhouette, offset)

            # Xử lý các sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Nếu người dùng đóng cửa sổ
                    pygame.quit()  # Thoát Pygame
                    sys.exit()  # Thoát chương trình
                if event.type == pygame.KEYDOWN:  # Nếu người dùng nhấn phím
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()  # Thoát Pygame
                        os.system(f"{sys.executable} menu.py")
                        sys.exit()  # Thoát chương trình
                    if event.key == pygame.K_a:
                        self.movement[0] = True  # Di chuyển sang trái
                    if event.key == pygame.K_d:
                        self.movement[1] = True  # Di chuyển sang phải
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        if self.player.jump():  # Nhảy
                            self.sfx['jump'].play()  # Phát âm thanh nhảy
                    if event.key == pygame.K_k:
                        self.player.dash()  # Lao
                    if self.phadao==False:
                        if event.key == pygame.K_1:
                            self.level=0
                            self.load_level(self.level)
                        if event.key == pygame.K_2:
                            self.level=1
                            self.load_level(self.level)
                        if event.key == pygame.K_3:
                            self.level=2
                            self.load_level(self.level)
                        if event.key == pygame.K_4:
                            self.level=3
                            self.load_level(self.level)
                        if event.key == pygame.K_5: 
                            self.level=4
                            self.load_level(self.level)
                if event.type == pygame.KEYUP:  # Nếu người dùng thả phím
                    if event.key == pygame.K_a:
                        self.movement[0] = False  # Ngừng di chuyển sang trái
                    if event.key == pygame.K_d:
                        self.movement[1] = False  # Ngừng di chuyển sang phải

            self.display_1.blit(self.display, (0, 0))  # Vẽ bề mặt hiển thị lên bề mặt hiển thị thứ hai
            self.screen.blit(pygame.transform.scale(self.display_1, self.screen.get_size()), (0, 0))

            pygame.display.update()  # Cập nhật màn hình
            self.clock.tick(60)  # Giới hạn tốc độ khung hình ở 60 FPS

Game().run()  # Chạy game
