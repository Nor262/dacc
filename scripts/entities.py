import math
import random

import pygame

class PhysicsEntity: # lớp cơ bản cho các thực thể trong trò chơi với các thuộc tính vật lí
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle') # thiết lập hành động ban đầu của thực thể là đứng yên
        
        self.last_movement = [0, 0]
    
    def rect(self): # trả về một hình chữ nhật đại diện cho vị trí và kích thức của thực thể ,dùng dể xác định va chạm
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action): # thiết lập hành động mới cho thực thể và cập nhật hoạt ảnh tương ứng
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, tilemap, movement=(0, 0)):# cập nhật trạng thái của thực thể
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False} #khi phương thức update() được gọi, trạng thái va chạm của thực thể được đặt là lại về False
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) # tính toán dựa trên chuyển động và vận tốc hiện tại của thực thể
        #cập nhật vị trí theo trục X:
        self.pos[0] += frame_movement[0] #Cập nhật vị trí thực thể theo trục X bằng cách thêm chuyển động trong khung hình hiện tại.
        entity_rect = self.rect() #Tạo hình chữ nhật đại diện cho vị trí và kích thước hiện tại của thực thể.
        for rect in tilemap.physics_rects_around(self.pos): #Lặp qua tất cả các hình chữ nhật vật lý xung quanh vị trí của thực thể.
            if entity_rect.colliderect(rect): #Kiểm tra xem có va chạm nào xảy ra giữa thực thể và các hình chữ nhật xung quanh.
                if frame_movement[0] > 0: #Nếu chuyển động theo trục X là dương (đi sang phải).
                    entity_rect.right = rect.left #Điều chỉnh vị trí của thực thể để đảm bảo không đi qua cạnh trái của hình chữ nhật va chạm.
                    self.collisions['right'] = True #Cập nhật trạng thái va chạm bên phải.
                if frame_movement[0] < 0: #Nếu chuyển động theo trục X là âm (đi sang trái).
                    entity_rect.left = rect.right #Điều chỉnh vị trí của thực thể để đảm bảo không đi qua cạnh phải của hình chữ nhật va chạm.
                    self.collisions['left'] = True #Cập nhật trạng thái va chạm bên trái.
                self.pos[0] = entity_rect.x #Cập nhật lại vị trí của thực thể theo trục X sau khi đã điều chỉnh va chạm.
        #cập nhật vị trí theo trục Y
        self.pos[1] += frame_movement[1] # cập nhật vị trí của thực thể theo trục Y bằng cách thêm chuyển động trong khung hình hiện tại.
        entity_rect = self.rect() #Tạo hình chữ nhật đại diện cho vị trí và kích thước hiện tại của thực thể.
        for rect in tilemap.physics_rects_around(self.pos): #Lặp qua tất cả các hình chữ nhật vật lý xung quanh vị trí của thực thể.
            if entity_rect.colliderect(rect): # Kiểm tra xem có va chạm nào xảy ra giữa thực thể và các hình chữ nhật xung quanh.
                if frame_movement[1] > 0: #Nếu chuyển động theo trục Y là dương (đi xuống dưới).
                    entity_rect.bottom = rect.top #Điều chỉnh vị trí của thực thể để đảm bảo không đi qua cạnh trên của hình chữ nhật va chạm.
                    self.collisions['down'] = True #Cập nhật trạng thái va chạm phía dưới.
                if frame_movement[1] < 0: #Nếu chuyển động theo trục Y là âm (đi lên trên)
                    entity_rect.top = rect.bottom #Điều chỉnh vị trí của thực thể để đảm bảo không đi qua cạnh dưới của hình chữ nhật va chạm.
                    self.collisions['up'] = True #Cập nhật trạng thái va chạm phía trên.
                self.pos[1] = entity_rect.y #Cập nhật lại vị trí của thực thể theo trục Y sau khi đã điều chỉnh va chạm.
                
        if movement[0] > 0: #Nếu chuyển động theo trục X là dương (đi sang phải), đặt self.flip về False (không lật hình ảnh).
            self.flip = False
        if movement[0] < 0: #Nếu chuyển động theo trục X là âm (đi sang trái), đặt self.flip về True (lật hình ảnh).
            self.flip = True
            
        self.last_movement = movement #Lưu trữ chuyển động cuối cùng để sử dụng trong các phép tính hoặc logic khác trong tương lai.
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1) #Cập nhật vận tốc theo trục Y bằng cách thêm một giá trị nhỏ để mô phỏng trọng lực. Vận tốc này được giới hạn ở mức 5.
        
        if self.collisions['down'] or self.collisions['up']: #Nếu có va chạm phía dưới hoặc phía trên, đặt lại vận tốc theo trục Y về 0. Điều này đảm bảo rằng thực thể không tiếp tục di chuyển qua các vật cản.
            self.velocity[1] = 0
            
        self.animation.update() #Gọi phương thức update() của đối tượng hoạt ảnh để cập nhật trạng thái của hoạt ảnh, đảm bảo hoạt ảnh chạy đúng theo thời gian.
        
    def render(self, surf, offset=(0, 0)): #Vẽ thực thể lên bề mặt (surf) với độ lệch xác định.
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        
class Enemy(PhysicsEntity): #Lớp này kế thừa từ PhysicsEntity và thêm các thuộc tính và phương thức đặc biệt cho kẻ thù.
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        
        self.walking = 0
        
    def update(self, tilemap, movement=(0, 0)):
        if self.walking: #Kiểm tra xem kẻ thù có đang ở trạng thái đi bộ không. self.walking là một bộ đếm để theo dõi thời gian đi bộ của kẻ thù.
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)): #Kiểm tra xem phía trước kẻ thù có phải là một vật cản không
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip #Nếu có va chạm bên phải hoặc bên trái, kẻ thù sẽ quay đầu (self.flip = not self.flip).
                else: #Nếu không có va chạm, kẻ thù sẽ tiếp tục di chuyển theo hướng hiện tại với tốc độ 0.5.
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else: ##Nếu có va chạm bên phải hoặc bên trái, kẻ thù sẽ quay đầu (self.flip = not self.flip)
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1]) #Tính khoảng cách đến người chơi
                if (abs(dis[1]) < 16): #Lấy giá trị tuyệt đối của khoảng cách theo trục Y.
                    if (self.flip and dis[0] < 0):#Kiểm tra xem kẻ thù có đang bị lật hay không (tức là quay mặt sang trái) và Kiểm tra xem người chơi có nằm bên trái của kẻ thù hay không.
                        self.game.sfx['shoot'].play() #Phát âm thanh bắn.
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0]) #Thêm một viên đạn vào danh sách projectiles của trò chơi.
                        #Viên đạn được tạo ra ở vị trí self.rect().centerx - 7, self.rect().centery (chỉnh vị trí để viên đạn xuất hiện từ đúng vị trí của kẻ thù).
                        #-1.5: Vận tốc theo trục X của viên đạn (bắn về phía bên trái).
                        #0: Vận tốc theo trục Y của viên đạn (không có chuyển động dọc).
                    if (not self.flip and dis[0] > 0): #Kiểm tra xem kẻ thù có không bị lật hay không (tức là quay mặt sang phải) và Kiểm tra xem người chơi có nằm bên phải của kẻ thù hay không.
                        self.game.sfx['shoot'].play() #Phát âm thanh bắn.
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                        # Viên đạn được tạo ra ở vị trí self.rect().centerx + 7, self.rect().centery (chỉnh vị trí để viên đạn xuất hiện từ đúng vị trí của kẻ thù).
                        # 1.5: Vận tốc theo trục X của viên đạn (bắn về phía bên phải).
                        # 0: Vận tốc theo trục Y của viên đạn (không có chuyển động dọc).
        elif random.random() < 0.01: #Với một xác suất nhỏ, kẻ thù sẽ bắt đầu đi bộ trong một khoảng thời gian ngẫu nhiên (từ 30 đến 120 khung hình).
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement) #Gọi phương thức update của lớp PhysicsEntity để cập nhật vị trí và trạng thái va chạm chung của kẻ thù.
        
        if movement[0] != 0: #Nếu có chuyển động theo trục X (movement[0] != 0), kẻ thù sẽ chuyển sang trạng thái run.
            self.set_action('run')
        else: #Nếu không, kẻ thù sẽ ở trạng thái idle.
            self.set_action('idle')
            
        if abs(self.game.player.dashing) >= 50: #Nếu người chơi đang lướt với tốc độ lớn (abs(self.game.player.dashing) >= 50) và va chạm với kẻ thù
            if self.rect().colliderect(self.game.player.rect()):# kẻ thù sẽ bị đánh trúng.
                self.game.screenshake = max(16, self.game.screenshake) #Kích hoạt hiệu ứng rung màn hình
                self.game.sfx['hit'].play() #Chơi âm thanh va chạm
                for i in range(30): #Vòng lặp tạo ra 30 hạt với các góc và tốc độ ngẫu nhiên để tạo hiệu ứng thị giác.
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                return True
            
    def render(self, surf, offset=(0, 0)): #Gọi phương thức render của lớp PhysicsEntity để vẽ thực thể (kẻ thù) lên bề mặt surf với độ lệch offset xác định. Điều này đảm bảo rằng các thuộc tính cơ bản như hình dạng và hoạt ảnh của kẻ thù được vẽ lên màn hình trước.
        super().render(surf, offset=offset)
        
        if self.flip: #Nếu self.flip là True, nghĩa là kẻ thù đang quay mặt sang trái.
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
            #pygame.transform.flip(self.game.assets['gun'], True, False) : Lật hình ảnh vũ khí theo trục X.
            #surf.blit(...): Vẽ hình ảnh vũ khí lên bề mặt surf.
            #(self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]): Tọa độ để vẽ hình ảnh vũ khí, được tính toán để đặt vũ khí ở đúng vị trí của kẻ thù.
            #self.rect().centerx - 4: Đặt vị trí ngang của vũ khí so với trung tâm của kẻ thù.
            #self.game.assets['gun'].get_width(): Đảm bảo vũ khí không bị vẽ ra ngoài biên của kẻ thù.
            #- offset[0], - offset[1]: Bù trừ độ lệch
        else: #Nếu self.flip là False, nghĩa là kẻ thù đang quay mặt sang phải
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))
            #surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1])): Vẽ hình ảnh vũ khí lên bề mặt surf mà không cần lật hình ảnh.
            #(self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]): Tọa độ để vẽ hình ảnh vũ khí, được tính toán để đặt vũ khí ở đúng vị trí của kẻ thù.
            #self.rect().centerx + 4: Đặt vị trí ngang của vũ khí so với trung tâm của kẻ thù.
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
    
    def update(self, tilemap, movement=(0, 0)): #super().update(tilemap, movement=movement): Gọi phương thức update của lớp PhysicsEntity để cập nhật vị trí và trạng thái va chạm cơ bản của người chơi.
        super().update(tilemap, movement=movement)
        
        self.air_time += 1 #Tăng thời gian người chơi ở trong không khí mỗi khung hình. Điều này được sử dụng để kiểm tra các trạng thái liên quan đến nhảy và trượt tường.
        
        if self.air_time > 120: # Nếu người chơi ở trong không khí quá lâu (hơn 120 khung hình), điều này có thể được coi là người chơi đã chết hoặc rơi ra ngoài bản đồ.
            if not self.game.dead: #Nếu người chơi chưa chết, kích hoạt rung màn hình (self.game.screenshake).
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1 #Tăng giá trị trạng thái "chết" của người chơi.
        
        if self.collisions['down']: #Nếu người chơi va chạm với mặt đất, đặt lại self.air_time về 0 và self.jumps về 1.
            self.air_time = 0
            self.jumps = 1
            
        self.wall_slide = False #Đặt trạng thái trượt tường ban đầu về False.
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4: #Nếu người chơi va chạm với tường và thời gian trong không khí lớn hơn 4 khung hình, chuyển sang trạng thái trượt tường.
            self.wall_slide = True #Đặt trạng thái trượt tường về True.
            self.velocity[1] = min(self.velocity[1], 0.5) #Giới hạn vận tốc theo trục Y để người chơi trượt tường chậm hơn.
            if self.collisions['right']: #Nếu va chạm với tường phải, đặt self.flip về False (quay mặt sang trái).
                self.flip = False
            else: #Nếu va chạm với tường trái, đặt self.flip về True (quay mặt sang phải).
                self.flip = True
            self.set_action('wall_slide') #Đặt hành động hiện tại là "trượt tường".
        
        if not self.wall_slide: #Nếu không trượt tường, kiểm tra các trạng thái khác.
            if self.air_time > 4:# Nếu thời gian trong không khí lớn hơn 4 khung hình, đặt hành động là "nhảy".
                self.set_action('jump')
            elif movement[0] != 0: #Nếu có chuyển động theo trục X, đặt hành động là "chạy".
                self.set_action('run')
            else: #Nếu không có chuyển động nào, đặt hành động là "đứng yên".
                self.set_action('idle')
        
        if abs(self.dashing) in {60, 50}: #Nếu trạng thái lướt là 60 hoặc 50 (bắt đầu hoặc kết thúc lướt), tạo hiệu ứng hạt.
            for i in range(20): #Vòng lặp tạo ra 20 hạt với các góc và tốc độ ngẫu nhiên để tạo hiệu ứng thị giác.
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
        if self.dashing > 0: #Nếu đang lướt về phía trước, giảm giá trị của self.dashing.
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0: #Nếu đang lướt về phía sau, tăng giá trị của self.dashing để tiến về 0.
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50: #Nếu trạng thái lướt lớn hơn 50, cập nhật vận tốc theo trục X.
            self.velocity[0] = abs(self.dashing) / self.dashing * 8 #Tính toán vận tốc theo hướng lướt.
            if abs(self.dashing) == 51: #Nếu trạng thái lướt là 51, giảm vận tốc theo trục X để tạo hiệu ứng giảm tốc.
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
          
        if self.velocity[0] > 0: #Nếu vận tốc theo trục X lớn hơn 0, giảm nó dần dần để đạt tới 0.
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else: #Nếu vận tốc theo trục X nhỏ hơn 0, tăng nó dần dần để đạt tới 0.
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
    
    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50: #Kiểm tra trạng thái lướt của người chơi. Nếu giá trị tuyệt đối của dashing nhỏ hơn hoặc bằng 50, người chơi sẽ được vẽ lên màn hình. Điều này có thể được sử dụng để tạo hiệu ứng đặc biệt khi người chơi đang lướt (chẳng hạn như làm mờ hoặc không hiển thị người chơi khi lướt quá nhanh).
            super().render(surf, offset=offset) #Gọi phương thức render của lớp PhysicsEntity để vẽ người chơi lên bề mặt surf với độ lệch offset xác định. Điều này đảm bảo rằng các thuộc tính cơ bản như hình dạng và hoạt ảnh của người chơi được vẽ lên màn hình.
    def jump(self):
        if self.wall_slide: #Nếu người chơi đang trượt tường.
            if self.flip and self.last_movement[0] < 0: #Nếu người chơi đang quay mặt sang trái và chuyển động cuối cùng là sang trái.
                self.velocity[0] = 3.5 #Đặt vận tốc theo trục X để nhảy sang phải.
                self.velocity[1] = -2.5 #Đặt vận tốc theo trục Y để nhảy lên.
                self.air_time = 5 #Đặt thời gian trong không khí để ngăn người chơi ngay lập tức rơi xuống.
                self.jumps = max(0, self.jumps - 1) #Giảm số lần nhảy còn lại.
                return True #Trả về True để chỉ ra rằng người chơi đã thực hiện hành động nhảy.
            elif not self.flip and self.last_movement[0] > 0: #Nếu người chơi đang quay mặt sang phải và chuyển động cuối cùng là sang phải.
                self.velocity[0] = -3.5 #Đặt vận tốc theo trục X để nhảy sang trái.
                self.velocity[1] = -2.5 #Đặt vận tốc theo trục Y để nhảy lên.
                self.air_time = 5 #Đặt thời gian trong không khí để ngăn người chơi ngay lập tức rơi xuống.
                self.jumps = max(0, self.jumps - 1) #Giảm số lần nhảy còn lại.
                return True #Trả về True để chỉ ra rằng người chơi đã thực hiện hành động nhảy.
                
        elif self.jumps: #Nếu người chơi còn lần nhảy.
            self.velocity[1] = -3 #Đặt vận tốc theo trục Y để nhảy lên.
            self.jumps -= 1 #Giảm số lần nhảy còn lại
            self.air_time = 5 #Đặt thời gian trong không khí để ngăn người chơi ngay lập tức rơi xuống.
            return True #Trả về True để chỉ ra rằng người chơi đã thực hiện hành động nhảy.
    
    def dash(self):
        if not self.dashing: #Nếu người chơi không đang lướt
            self.game.sfx['dash'].play() #Phát âm thanh lướt.
            if self.flip: #Nếu người chơi đang quay mặt sang trái.
                self.dashing = -60 #Đặt giá trị dashing là -60 để lướt sang trái.
            else: #Nếu người chơi đang quay mặt sang phải.
                self.dashing = 60 #Đặt giá trị dashing là 60 để lướt sang phải.
