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
title('ԭͼ')

subplot(2,2,2)
imshow(im_use_mask);
title('ʹ����Ĥ')

subplot(2,2,3)
imshow(im_abs_mask);
title('ʹ�ñ궨�����Ĥ')

subplot(2,2,4)
imshow(im_enhanced);
title('����ԭͼ')



figure(2)
h = fspecial('laplacian', 1)
% 'replicate', ͼ���Сͨ��������߽��ֵ����չ
% im_after2 = imfilter(im1, h, 'replicate');
% im_after2 = imfilter(im1, h);
% �����ó��Ļ���������ͼ��
im_use_mask2 = im1;
im_enhanced2 = im1;
im_use_mask2 = imfilter(im1, mask);
%����ԭͼ
im_enhanced2 = im_use_mask2 + im1;


subplot(2,2,1)
imshow(im_use_mask);
title('�Լ�ʵ�ֵ�ʹ����Ĥ���ͼ��')

subplot(2,2,2)
imshow(im_use_mask2);
title('����ʵ�ֵ�ʹ����Ĥ���ͼ��')

subplot(2,2,3)
imshow(im_enhanced);
title('�Լ�ʵ�ֵ�������˹��ǿ')

subplot(2,2,4)
imshow(im_enhanced2);
title('����ʵ�ֵ�������˹��ǿ')

% ������˹ͼ����ǿ
function [im_use_mask, im_enhanced, im_abs_mask] = my_filter(im0, mask)
%��������ֱ���ԭͼ����Ĥ
%���ش�����ͼ��
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