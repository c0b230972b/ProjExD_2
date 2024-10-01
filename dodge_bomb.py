import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん、または、爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """

    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def game_over(t) -> int:
    """
    引数：GameOver画面を表示する秒数
    """
    return time.sleep(t)

def expan_bb():
    bb_accs = [a for a in range(1, 11)]  # 加速度のリスト
    bb_imgs= []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_accs, bb_imgs

    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200 
    #bb_img = pg.Surface((20, 20))  # 空のSurface
    #bb_img.set_colorkey((0, 0, 0))  # 爆弾の四隅を透過させる
    #pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    
    
    vx, vy = +5, +5  # 爆弾の速度
    bb_accs, bb_imgs = expan_bb()
    bb_img = bb_imgs[min(tmr//500, 9)]
    go_img = pg.Surface((WIDTH,HEIGHT))
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    pg.draw.rect(go_img,(0, 0, 0), (0, 0, WIDTH, HEIGHT)) #(Surface, (色), (左上のX, 左上のy, 横幅, 縦幅))
    go_img.set_alpha(200)
    go_rct = go_img.get_rect()
    go_rct = 0, 0
    ck_img = pg.image.load("fig/8.png")
    ck_rct = ck_img.get_rect()
    ck_rct.center = (WIDTH//3, HEIGHT//2)
    ck_img2 = pg.image.load("fig/8.png")
    ck_rct2 = ck_img2.get_rect()
    ck_rct2.center = ((WIDTH//3)*2, HEIGHT//2)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            # こうかとんが爆弾と重なっていたら
            screen.blit(go_img, go_rct)
            screen.blit(ck_img, ck_rct)
            screen.blit(ck_img2, ck_rct2)
            screen.blit(txt,[WIDTH//3 +30, HEIGHT//2 -20])
            pg.display.update()
            game_over(5)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # [横座標, 縦座標]
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横座標
                sum_mv[1] += tpl[1]  # 縦座標
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        
        screen.blit(kk_img, kk_rct)

        
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
