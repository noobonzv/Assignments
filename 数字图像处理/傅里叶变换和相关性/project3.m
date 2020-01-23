clc;

% �����������

% 4.2.a
im = imread('Fig4.18(a).jpg');
F = im;
F_norm = im;
% ����Ƶ�ף��ڶ����ǹ�һ����Ƶ��
[F, F_norm] = compute_spectrum(im);


% 4.2.b
% ͼ��Ƶ��
figure;
subplot(121);
imshow(im);
title('Fig.4.18(a)ԭͼ');
subplot(122);
imshow(F_norm);
title('Fig.4.18(a)�ĸ���ҶƵ��');


% 4.2.c
% ���ؾ�ֵ

[m,n] = size(im);
sum0 = sum(sum(im));
avg = sum0 / m / n
im = abs(fft2(im));
avg2 = im(1,1) / m / n


% 4.3.b
% ��˹��ͨ
im = imread('Fig4.11(a).jpg');
[m,n] = size(im);
% ���һ�������� ��׼��sigma
im_after = gaussian_lowpass(im, m/2, n/2, 15);
figure;
subplot(121);
imshow(im);
title('Fig4.11(a)ԭͼ');
subplot(122);
imshow(im_after,[]);
title('Fig4.11(a)������˹��ͨ�˲���');


% 4.4.a
% ��ȥ����Ľ��
img44a = uint8(im) - uint8(im_after);
figure;
subplot(121);
imshow(im);
title('Fig4.18(a)ԭͼ');
subplot(122);
imshow(img44a);
title('Fig.4.18(a)��ȥ4.3.b�Ľ��');

% 4.4.b
% ���Ĳ�ͬ�� sigma
figure;
subplot(231);
imshow(im);
title('Fig4.18(a)ԭͼ');
sigmas = [15, 30, 50, 80, 100];
for i = 1:5
    im_after_i = gaussian_lowpass(im, m/2, n/2, sigmas(i));
    img44b = uint8(im) - uint8(im_after_i);
    subplot(2,3,i+1);
    imshow(img44b);
    title(['Fig.4.18(a)��ȥ4.3.b�Ľ��, sigma = ', num2str(sigmas(i))]);
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
% ��չͼƬ
im_expand1(1:m1,1:n1) = im_a;
im_expand2(1:m2,1:n2) = im_b;
% ���Ļ�
im_expand1 = shift_to_center(im_expand1);
im_expand2 = shift_to_center(im_expand2);
% ����Ҷ���仯
F1 = fft2(im_expand1);
F2 = fft2(im_expand2);
% ����һ��ȡ����
% ��������������ͬ��F1ȡ������ӽ���ʵ���
correlation = F2 .* conj(F1);
% ���仯���ƶ�������
result = shift_ifft(ifft2(correlation));

figure;
subplot(121);
imshow(uint8(im_a));
title('Fig4.41(a)ԭͼ');
subplot(122);
imshow(uint8(im_b));
title('Fig4.41(b)ԭͼ');
figure;
imshow(result,[]);
title('Fig4.41(a)(b)�����')
% ��������ĵط�
maximum  = max(max(result));
[row,col] = find(result == maximum);
% ȡ���������ߵ�һ��
% pic = result(160:220,[160:220]);
% imshow(pic,[]);
disp([row,col]);



% �����ת����ҶƵ�׵ı仯
im404 = imread('Fig4.04(a).jpg');
figure,
subplot(231),imshow(im404);
title('Fig4.04(a)ԭͼ')
[F0,F00] = compute_spectrum(im404);
subplot(232);
imshow(F00);
title('ԭͼ�ĸ���ҶƵ��')
for i = 1:4
    im404_45 = imrotate(im404,45*i);
    [F1,F11] = compute_spectrum(im404_45);
    subplot(2,3,i+2);
    imshow(F11);
    title(['��ת',num2str(i*45), '���ĸ���ҶƵ��'])
end




% 4.1.a
% Ƶ�����Ļ�
% ����Ϊͼ��
% ���Ϊ���Ļ����ͼ��
function  im = shift_to_center(img)
	[m, n] = size(img);
    % ����double������, ����ÿ������ֵ����������
    im = double(img);
    for i =  1:m
        for j = 1:n
            im(i,j) = im(i,j)*((-1)^(i+j));
        end
    end
end


% 4.1.b
% ����H ��Ƶ���˲���F�Ǹ���Ҷ�任���Ƶ��
% ���Ǻ������Ŀ����˼��������õ���дһ������...
function Y = mul(H,F)
	Y = H .* F;
end

% 4.1.c
% ���㸵��Ҷ���仯
% ������ͼ�����ֱ�ӵ��⣬���ظ���ҶƵ�ף�����
function im2= my_ifft(im)
% ����Ҷ���任
im2 = ifft2(im);
% ȡʵ��
% im2 = real(im2);
% im2 = shift_to_center(im2);
end


% 4.1.d
% Multiply the result by (-1)^x+y and take the real part.
% ���任�Ľ��ȡʵ����ƽ��
function im = shift_ifft(res)
	im = shift_to_center(real(res));
end


% 4.1.e
% ���任��Ƶ�ף���������
% ���صĵ�һ��������Ƶ�ף��ڶ����ǹ�һ��Ƶ��
function [im, im_norm] = compute_spectrum(img)
% ���Ļ�
im = shift_to_center(img);
% fft2 ����Ǹ�������ģ
im = abs(fft2(im));
% ��Щֵ�Ƚϴ�+1ȡlog
% im = double(log(im+1));
im = double( im .^ 0.2);
% []�ǽ�����ӳ�䵽0~1
% ��һ��
min_v = min(min(im));
max_v = max(max(im));
im_norm = double( (im-min_v) ./ (max_v-min_v) );
% imshow(im, []);
end


% 4.3.a
% ��˹��ͨ�˲�
% ����Ĳ�������Ϊͼ�����ƽ�����꣬��˹��ͨ�˲��ı�׼��
function im_after = gaussian_lowpass(img,x0,y0,sig)
	[m,n] = size(img);
	% Ƶ�����Ļ�
	img = shift_to_center(img);
	% ���任
	F= fft2(img);
    % ����ת��double����Ȼ�� H .* F ˵��֧�ָ�����
    H = double(img);
    im_after = img;
	for i = 1:m
		for j = 1:n
			D2 = (i-x0)^2 + (j-y0)^2;
			H(i,j) = exp(-0.5* ( D2 / sig^2 ) );
		end
    end
	% �˲�
    im_after = H .* F;
	% ���任
	im_after = ifft2(im_after);
	% ƽ��
	im_after = shift_ifft(im_after);
end

