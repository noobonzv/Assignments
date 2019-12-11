% im = imread('test1.jpg');
% im = rgb2gray(im);
im0 = imread('Fig0308(a)(fractured_spine).tif');
% 为了方便统计频率，就没有转换为double
im = uint8(im0)
[x,y] = size(im);
% disp(size(im))

% 1*256矩阵，记录概率
p_gray_scale = zeros(1,256);

% 对个灰度值计数算频率
% 注意像素是 [0,255]， 矩阵下标是从1开始
for i = 0:255
    times = length(find(im==i));
    p_gray_scale(i+1) = times / (x*y);
end

% 累积函数
P = zeros(1,256);
P(1) = p_gray_scale(1);
for i = 2: 256
    P(i) = P(i-1) + p_gray_scale(i);
end

% 变换的图片
s = round(P*255);
pic_after_process = im;
% 这里不用双重循环可以稍微提高效率
for i = 0: 255
    pic_after_process(find(im==i)) = s(i+1);
end

% 变换后的图片的灰度频率
p_gray_scale_after =  zeros(1,256);
for i=0:255  
    times = length(find(pic_after_process==i));
    p_gray_scale_after(i+1) = times / (x*y);            
end  

figure(1)
subplot(1,2,1);
imshow(im);  
title('原图');  

% figure(2) 
subplot(1,2,2);
imshow(pic_after_process)                            
title('均衡化后的图像');  

figure(2)
subplot(2,1,1);  
bar(0:255,p_gray_scale,'b');  
title('原图的直方图');  

subplot(2,1,2);  
bar(0:255,p_gray_scale_after,'b');
title('均衡化后的图片的直方图'); 
