clc;

% 函数放在最后

% 4.2.a
im = imread('Fig4.18(a).jpg');
F = im;
F_norm = im;
% 计算频谱，第二个是归一化的频谱
[F, F_norm] = compute_spectrum(im);


% 4.2.b
% 图像频谱
figure;
subplot(121);
imshow(im);
title('Fig.4.18(a)原图');
subplot(122);
imshow(F_norm);
title('Fig.4.18(a)的傅里叶频谱');


% 4.2.c
% 像素均值

[m,n] = size(im);
sum0 = sum(sum(im));
avg = sum0 / m / n
im = abs(fft2(im));
avg2 = im(1,1) / m / n


% 4.3.b
% 高斯低通
im = imread('Fig4.11(a).jpg');
[m,n] = size(im);
% 最后一个参数是 标准差sigma
im_after = gaussian_lowpass(im, m/2, n/2, 15);
figure;
subplot(121);
imshow(im);
title('Fig4.11(a)原图');
subplot(122);
imshow(im_after,[]);
title('Fig4.11(a)经过高斯低通滤波后');


% 4.4.a
% 减去上面的结果
img44a = uint8(im) - uint8(im_after);
figure;
subplot(121);
imshow(im);
title('Fig4.18(a)原图');
subplot(122);
imshow(img44a);
title('Fig.4.18(a)减去4.3.b的结果');

% 4.4.b
% 更改不同的 sigma
figure;
subplot(231);
imshow(im);
title('Fig4.18(a)原图');
sigmas = [15, 30, 50, 80, 100];
for i = 1:5
    im_after_i = gaussian_lowpass(im, m/2, n/2, sigmas(i));
    img44b = uint8(im) - uint8(im_after_i);
    subplot(2,3,i+1);
    imshow(img44b);
    title(['Fig.4.18(a)减去4.3.b的结果, sigma = ', num2str(sigmas(i))]);
end



% 4.5
% 
im_a = imread('Fig4.41(a).jpg');
im_b = imread('Fig4.41(b).jpg');
[m1,n1] = size(im_a);
[m2,n2] = size(im_b);
P = m1 + m2;
Q = n1+ n2;
im_expand1 = zeros(P,Q);
im_expand2 = zeros(P,Q);
% 扩展图片
im_expand1(1:m1,1:n1) = im_a;
im_expand2(1:m2,1:n2) = im_b;
% 中心化
im_expand1 = shift_to_center(im_expand1);
im_expand2 = shift_to_center(im_expand2);
% 傅里叶正变化
F1 = fft2(im_expand1);
F2 = fft2(im_expand2);
% 其中一个取共轭
% 不过交换后结果不同，F1取共轭更接近真实情况
correlation = F2 .* conj(F1);
% 反变化后移动到中心
result = shift_ifft(ifft2(correlation));

figure;
subplot(121);
imshow(uint8(im_a));
title('Fig4.41(a)原图');
subplot(122);
imshow(uint8(im_b));
title('Fig4.41(b)原图');
figure;
imshow(result,[]);
title('Fig4.41(a)(b)相关性')
% 相关性最大的地方
maximum  = max(max(result));
[row,col] = find(result == maximum);
% 取出相关性最高的一块
% pic = result(160:220,[160:220]);
% imshow(pic,[]);
disp([row,col]);



% 检测旋转后傅里叶频谱的变化
im404 = imread('Fig4.04(a).jpg');
figure,
subplot(231),imshow(im404);
title('Fig4.04(a)原图')
[F0,F00] = compute_spectrum(im404);
subplot(232);
imshow(F00);
title('原图的傅里叶频谱')
for i = 1:4
    im404_45 = imrotate(im404,45*i);
    [F1,F11] = compute_spectrum(im404_45);
    subplot(2,3,i+2);
    imshow(F11);
    title(['旋转',num2str(i*45), '°后的傅里叶频谱'])
end




% 4.1.a
% 频谱中心化
% 输入为图像
% 输出为中心化后的图像
function  im = shift_to_center(img)
	[m, n] = size(img);
    % 不加double有问题, 后面每个像素值会变成两倍？
    im = double(img);
    for i =  1:m
        for j = 1:n
            im(i,j) = im(i,j)*((-1)^(i+j));
        end
    end
end


% 4.1.b
% 输入H 是频率滤波，F是傅里叶变换后的频谱
% 不是很理解题目的意思，这好像不用单独写一个函数...
function Y = mul(H,F)
	Y = H .* F;
end

% 4.1.c
% 计算傅里叶反变化
% 输入是图像矩阵，直接调库，返回傅里叶频谱，复数
function im2= my_ifft(im)
% 傅里叶反变换
im2 = ifft2(im);
% 取实部
% im2 = real(im2);
% im2 = shift_to_center(im2);
end


% 4.1.d
% Multiply the result by (-1)^x+y and take the real part.
% 反变换的结果取实部后平移
function im = shift_ifft(res)
	im = shift_to_center(real(res));
end


% 4.1.e
% 正变换算频谱，整个流程
% 返回的第一个参数是频谱，第二个是归一化频谱
function [im, im_norm] = compute_spectrum(img)
% 中心化
im = shift_to_center(img);
% fft2 结果是复数，求模
im = abs(fft2(im));
% 这些值比较大，+1取log
% im = double(log(im+1));
im = double( im .^ 0.2);
% []是将像素映射到0~1
% 归一化
min_v = min(min(im));
max_v = max(max(im));
im_norm = double( (im-min_v) ./ (max_v-min_v) );
% imshow(im, []);
end


% 4.3.a
% 高斯低通滤波
% 输入的参数依次为图像矩阵，平移坐标，高斯低通滤波的标准差
function im_after = gaussian_lowpass(img,x0,y0,sig)
	[m,n] = size(img);
	% 频谱中心化
	img = shift_to_center(img);
	% 正变换
	F= fft2(img);
    % 必须转成double，不然后 H .* F 说不支持复整数
    H = double(img);
    im_after = img;
	for i = 1:m
		for j = 1:n
			D2 = (i-x0)^2 + (j-y0)^2;
			H(i,j) = exp(-0.5* ( D2 / sig^2 ) );
		end
    end
	% 滤波
    im_after = H .* F;
	% 反变换
	im_after = ifft2(im_after);
	% 平移
	im_after = shift_ifft(im_after);
end

