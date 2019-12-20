clc
im = imread("Fig3.40(a).jpg");
im1 =im2double(im);
[x1, y1] = size(im1);

mask = [-1,-1,-1;-1,8,-1;-1,-1,-1];

im_use_mask= im1;
im_enhanced = im1;
im_abs_mask = im1;

[im_use_mask, im_enhanced, im_abs_mask] = my_filter(im1, mask);
figure(1)
subplot(2,2,1)
imshow(im1);
title('原图')

subplot(2,2,2)
imshow(im_use_mask);
title('使用掩膜')

subplot(2,2,3)
imshow(im_abs_mask);
title('使用标定后的掩膜')

subplot(2,2,4)
imshow(im_enhanced);
title('加上原图')



figure(2)
h = fspecial('laplacian', 1)
% 'replicate', 图像大小通过复制外边界的值来扩展
% im_after2 = imfilter(im1, h, 'replicate');
% im_after2 = imfilter(im1, h);
% 这样得出的还不是最后的图像
im_use_mask2 = im1;
im_enhanced2 = im1;
im_use_mask2 = imfilter(im1, mask);
%加上原图
im_enhanced2 = im_use_mask2 + im1;


subplot(2,2,1)
imshow(im_use_mask);
title('自己实现的使用掩膜后的图像')

subplot(2,2,2)
imshow(im_use_mask2);
title('调库实现的使用掩膜后的图像')

subplot(2,2,3)
imshow(im_enhanced);
title('自己实现的拉普拉斯增强')

subplot(2,2,4)
imshow(im_enhanced2);
title('调库实现的拉普拉斯增强')

% 拉普拉斯图像增强
function [im_use_mask, im_enhanced, im_abs_mask] = my_filter(im0, mask)
%输入参数分别是原图像，掩膜
%返回处理后的图像
    im = im2double(im0);
    [x,y] = size(im)
    im_enhanced = im;
    im_abs_mask = im
    im_use_mask = im;
    for i = 2: x-1
        for j = 2: y-1
            neighbor = im([i-1,i,i+1], [j-1,j,j+1]);
            im_use_mask(i,j) = sum(sum(neighbor .* mask));
            im_abs_mask(i, j) = abs(im_use_mask(i,j));
            im_enhanced(i, j) =  im(i,j) + im_use_mask(i,j);
           
        end
    end
end