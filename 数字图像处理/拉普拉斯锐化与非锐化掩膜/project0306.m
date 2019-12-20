clc
im = imread("Fig3.43(a).jpg");
im1 =im2double(im);
[x1, y1] = size(im1);

% ��ֵ Afxy - favg
im_enhanced = im1;
A = 2.8;

im_enhanced= my_h_boost_filter_avg(im1, A);
figure(1)
subplot(1,2,1)
imshow(im1);
title('ԭͼ')

subplot(1,2,2)
imshow(im_enhanced);
title('�������˲�')
title(['A = ', num2str(A)]);


% ������˹
figure(2)
im_enhanced2 = im1;
A = 1.7;

im_enhanced2 = my_h_boost_filter_lpls(im1, A);
subplot(1,2,1)
imshow(im1);
title('ԭͼ')

subplot(1,2,2)
imshow(im_enhanced2);
title('������˹�������˲�')
 title(['A = ', num2str(A)]);


% ��ֵ
function im_enhanced = my_h_boost_filter_avg(im0, A)
%��������ֱ���ԭͼ��ϵ��
%���ش�����ͼ��
%     im = double(im0);
    im = im2double(im0);
    [x,y] = size(im)
    im_enhanced = im;
    for i = 2: x-1
        for j = 2: y-1
            neighbor = im([i-1,i,i+1], [j-1,j,j+1]);
            avg(i,j) = sum(sum(neighbor))/9;
            im_enhanced(i, j) =  A*im(i,j) - avg(i,j);
        end
    end
end


% ����������˹
function im_enhanced = my_h_boost_filter_lpls(im0, A)
%��������ֱ���ԭͼ��ϵ��
%���ش�����ͼ��
%     im = double(im0);
    im = im2double(im0);
    [x,y] = size(im)
    im_enhanced = im;
    mask = [-1,-1,-1;-1,A+8,-1;-1,-1,-1]
    for i = 2: x-1
        for j = 2: y-1
            neighbor = im([i-1,i,i+1], [j-1,j,j+1]);
            im_enhanced(i, j) =  sum(sum(neighbor .* mask));
        end
    end
end