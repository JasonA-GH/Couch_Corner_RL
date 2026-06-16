import pygame
import math
import sys

#start size
#point resolution
#x y
#current surface area

#walls = 
# y < 5 : x > 1
# y > 6
# x < -1
# x > 1 : y < 5

# start = 0, 0
# goal  = 5, 5

#start_size = 2 # 2x2 m

pygame.display.init()
pygame.font.init()
pygame.key.set_repeat(100)

screen = pygame.display.set_mode((1000,800))
pygame.display.set_caption('Game')

#board_image = pygame.image.load("Board_Stand.png")

#menu_image = pygame.image.load("MenuArea.png")

#red_disc = pygame.image.load("Red.png")
#yellow_disc = pygame.image.load("Yellow.png")


training = True
if(len(sys.argv) > 1):
    if(int(sys.argv[1]) == 0):
        training = False
running = True
debug = False
#gameStarted = False
#gameEnded = False

#start = 100
#circle_radius = 75
#offset = circle_radius*2+10
#round_x = [start+i*offset for i in range(7)]

#red_disc = pygame.transform.scale(red_disc, (circle_radius*2, circle_radius*2))
#yellow_disc = pygame.transform.scale(yellow_disc, (circle_radius*2, circle_radius*2))

clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 35)
#endFont = pygame.font.SysFont('PERTILI.TTF', 75)
#titleFont = pygame.font.SysFont('Times New Roman', 50)

debug_text = font.render("F3 = ON\nF4 = OFF", False, (255,255,255))

#red_name = font.render("AI", False, (255,255,255))
#yellow_name = font.render("You", False, (0,255,0))
#WinLoseText = font.render("", False, (0,255,0))
#title = titleFont.render("Connect 4", False, (255,255,255))

resolution = 200 # resolution of verticies along the perimiter of the square
x_len = 100
y_len = 200
verts = []

angle = 0

goal = (450, 550)
opp_goal = (150, 200)

def dist_to(p1, p2):
    return math.sqrt(math.pow(abs(p1[0]-p2[0]), 2)+ math.pow(abs(p1[1]-p2[1]), 2))

def dir_to_hall(x, y):
    #walls = 
    # y < 500 : x > 200
    # y > 600
    # x < 100
    # x > 200 : y < 500
    if(x > 200 and y < 500):
        #if polys center is to the left go left other wise go up
        return (-1, 0)
    elif(x < 100):
        return (1, 0)
    elif(y > 600):
        return (0, -1)
    elif(y < 0):
        return (0, 1)
    return (0,0)

def in_wall(x,y):
    return dir_to_hall(x,y) != (0,0)

def polygon_center():
    global verts
    cx = sum(x for x, y in verts) / len(verts)
    cy = sum(y for x, y in verts) / len(verts)
    return (cx, cy)

def closest_point_on_segment(px, py, ax, ay, bx, by):
    """Closest point on segment AB to point P"""
    dx = bx - ax
    dy = by - ay
    seg_len_sq = dx*dx + dy*dy
    
    if seg_len_sq == 0:
        return (ax, ay)  # segment is a point
    
    # t is how far along the segment the closest point is (0-1)
    t = ((px - ax) * dx + (py - ay) * dy) / seg_len_sq
    t = max(0, min(1, t))  # clamp to segment
    
    return (ax + t * dx, ay + t * dy)

"""def closest_point_on_polygon(px, py, vertices):
    #Closest point on polygon boundary to external point (px, py)
    min_dist = float('inf')
    closest = None
    
    n = len(vertices)
    for i in range(n):
        ax, ay = vertices[i]
        bx, by = vertices[(i + 1) % n]  # wrap around to first vertex
        
        cx, cy = closest_point_on_segment(px, py, ax, ay, bx, by)
        dist = (cx - px)**2 + (cy - py)**2  # squared is fine for comparison
        
        if dist < min_dist:
            min_dist = dist
            closest = (cx, cy)
    
    return closest"""

def closest_point_on_polygon(px, py, vertices): #ignores in wall
    min_dist = float('inf')
    closest = None
    
    n = len(vertices)
    for i in range(n):
        ax, ay = vertices[i]
        bx, by = vertices[(i + 1) % n]
        
        # Skip this edge if either endpoint is in a wall
        if in_wall(ax, ay) or in_wall(bx, by):
            continue
        
        cx, cy = closest_point_on_segment(px, py, ax, ay, bx, by)
        dist = (cx - px)**2 + (cy - py)**2
        
        if dist < min_dist:
            min_dist = dist
            closest = (cx, cy)
    
    return closest if closest is not None else (px, py)

def teleport_to_edge(p):
    #Teleport to polygon (This should fix the stranded vertex issue)

    global verts

    return closest_point_on_polygon(p[0], p[1], verts)

    start_p = p
    p = polygon_center()
    
    closest = 1000
    v = (0,0)
    for x,y in verts:
        if(x == p[0] and y == p[1]):
            #print("ASD")
            continue
        if(in_wall(x,y)):
            d = dist_to((x,y), p)
            if(d < closest):
                closest = d
                v = (x,y)

    if(v[0] == 0 and v[1] == 0):
        return p
                
    if(v[1] > p[1]):
        v = (v[0], v[1]+1)
    else:
        v = (v[0], v[1]-1)
    return v
    
def adjust_vert(x, y):

    if(in_wall(x,y)):
        (x,y) = teleport_to_edge((x,y))
    return (x,y)

def adjust_vert_slide(x, y):

    #Right wall Ceiling
    if(x >= 200 and (y >= 495 and y < 500)):
        y = 500
        #print("RIGHT WALL CEILING")
        #(x,y) = teleport_to_edge((x,y))
    else:
        #Right wall Wall
        if y < 500:
            if x > 200:
                x = 200
                #print("RIGHT WALL WALL")
                #(x,y) = teleport_to_edge((x,y))
                

    #Floor
    if y > 600:
        y = 600
        #print("FLOOR")
        #(x,y) = teleport_to_edge((x,y))

    #Ceiling_Top
    if(y < 0):
        y = 0
        #print("CELING TOP")
        #(x,y) = teleport_to_edge((x,y))

    #Left wall
    if(x < 100):
        x = 100
        #print("LEFT WALL")
        #(x,y) = teleport_to_edge((x,y))

    return (x, y)

def reset_polygon():
    global verts
    global x_len
    global y_len
    verts = []
    d = 0
    x = 0
    y = 0
    starting_offset_x = 100
    starting_offset_y = 300
    size_mod_x = x_len/(resolution/4)
    size_mod_y = y_len/(resolution/4)
    x_gap = 0
    y_gap = 0

    for i in range(resolution):
        if(d == 0):
            y += size_mod_y
            if(y >= y_len):
                d += 1
            #verts.append((starting_offset_x+x, starting_offset_y+y))
        elif(d == 1):
            x += size_mod_x
            if(x >= x_len):
                d += 1
            #verts.append((starting_offset_x+x, starting_offset_y+y))
        elif(d == 2):
            y -= size_mod_y
            if(y == 0):
                d += 1
            #verts.append((starting_offset_x+x, starting_offset_y+y))
        else:
            x -= size_mod_x
        verts.append(adjust_vert_slide(starting_offset_x+x, starting_offset_y+y))
        #print(verts[-1])
reset_polygon()
def rotate_polygon(angle_deg):
    global verts
    cx, cy = polygon_center()
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    #rotated = []
    for i, (x, y) in enumerate(verts):
        # Translate to origin
        dx = x - cx
        dy = y - cy
        # Rotate
        nx = dx * cos_a - dy * sin_a
        ny = dx * sin_a + dy * cos_a

        (nx, ny) = adjust_vert(nx + cx, ny + cy)
        verts[i] = (nx,ny)
        # Translate back
        #rotated.append((nx, ny))
    
    #return rotated
    #verts = rotated

def move_polygon(dx, dy):
    global verts
    #vs = []
    for i, (x, y) in enumerate(verts):
        nx = x+dx
        ny = y+dy

        (nx, ny) = adjust_vert(nx, ny)

        verts[i] = (nx,ny)
        #vs.append((nx, ny))

    #verts = vs
    #return vs
        

def dist_to_end():
    global verts
    (x,y) = polygon_center()
    return dist_to((x,y), goal)

def dist_to_opp_end():
    global verts
    (x,y) = polygon_center()
    return math.sqrt(math.pow(abs(x-opp_goal[0]), 2)+ math.pow(abs(y-opp_goal[1]), 2))

def polygon_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2

def get_surface_area():
    global verts
    #print(polygon_area(verts))
    return polygon_area(verts)


#while running:

def draw():
    global verts
    global debug
    clicked_once = False
    clock.tick(60)
    #clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if(event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
         #   if(event.mod &

    if(not training):
        keys = pygame.key.get_pressed()

        if(keys[pygame.K_F3]):
            debug = True
        if(keys[pygame.K_F4]):
            debug = False

        if keys[pygame.K_w]:
            move_polygon(0,-1)
        if keys[pygame.K_s]:
            move_polygon(0, 1)
        if keys[pygame.K_a]:
            move_polygon(-1, 0)
        if keys[pygame.K_d]:
            move_polygon(1, 0)
        if keys[pygame.K_q]:
            rotate_polygon(-1)
        if keys[pygame.K_e]:
            rotate_polygon(1)

        if(dist_to_end() < 100):
            print("You win!", get_surface_area())

    screen.fill((32,40,48))

    pygame.draw.polygon(screen, (0,0,0), [(200,0), (200, 500), (2000, 500), (2000, 600), (100, 600), (100, 0)])
    
    if(pygame.mouse.get_pressed(num_buttons=3)[0] and not clicked_once):
        print(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], in_wall(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        #verts = rotate_polygon(verts, 1, polygon_center(verts))
        #move_polygon(-1,-1)
        clicked_once = True
        print(get_surface_area(), polygon_center()[0]-150)
    if(pygame.mouse.get_pressed(num_buttons=3)[2] and not clicked_once):
        #print(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], in_wall(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        #rotate_polygon(15)
        #verts = move_polygon(10,0)
        clicked_once = True
        print(dist_to_end(), dist_to_opp_end())
        #get_surface_area(verts)
    if(not pygame.mouse.get_pressed(num_buttons=3)[0] and not pygame.mouse.get_pressed(num_buttons=3)[1]):
        clicked_once = False

    pygame.draw.polygon(screen, (255,255,255), verts)
    #verts = rotate_polygon(verts, angle, polygon_center(verts))

    #screen.blit(menu_image, (1285, 0))
    #screen.blit(board_image, (0,0))
    pygame.draw.circle(screen, (0,255,0), goal, 25) # goal
    pygame.draw.circle(screen, (255,0,0), opp_goal, 25) # opp goal
    

    if(debug):
        pygame.draw.circle(screen, (100,100,100), polygon_center(), 5)
        for x in verts:
            pygame.draw.circle(screen, (0,0,255), x, 3)
            
    
    #screen.blit(red_disc, (1350,550))
    #screen.blit(yellow_disc, (1650, 550))

    if(debug):
        screen.blit(debug_text, (0,0))

    pygame.display.flip()

if(not training):
    while True:
        draw()
    
def exit():
    pygame.quit()
