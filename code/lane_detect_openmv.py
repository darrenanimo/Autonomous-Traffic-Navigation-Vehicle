# Untitled - By: tjoye - Wed May 3 2023

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()
high_threshold = [90] #has max of 100
max_right_line = 0
max_left_line = 0
max_right   = 0
max_left = 0


while(True):
    clock.tick()
    print(clock.fps())

    roi=(0,120,320,240)

    img = sensor.snapshot()
    img = img.binary([high_threshold]) #choose one
    #img = img.laplacian(1, add =2, mul =2) #choose one

    for l in img.find_lines(roi=roi,threshold = 2000,x_stride=2, y_stride=1):
        if l.theta() !=89 and l.theta() != 0:
            #a = img.draw_line(l.line(), color = (0, 0, 255), thickness=3)
            if l.x1() >= max_left:
                max_left = l.x1()
                max_left_line = l
            if l.x2() <= max_right:
                max_right = l.x2()
                max_right_line = l
    if max_right_line != 0:
        a = img.draw_line(max_right_line.line(), color = (255, 0, 0), thickness=3)
        line_right = max_right_line.x2()
    else:
        line_right = 0
    if max_left_line != 0:
        a = img.draw_line(max_left_line.line(), color = (255, 0, 0), thickness=3)
        line_left = max_left_line.x1()
    else:
        line_left = 0

    lane_center = (line_left+line_right)//2
    print(lane_center)
    print(line_left)
    print(line_right)
    a = img.draw_arrow(160, 240, lane_center, 120, (0,0,255), thickness=3)
