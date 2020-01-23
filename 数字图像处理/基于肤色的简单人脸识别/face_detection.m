clc;

% im = imread('multi_face.jpg');
title('ԭͼ');
im = imread('test4.jpg');
% im = imread('one_face_h.jpg');
% im = imread('t2.jpg');
imshow(im);
[m,n,k] = size(im)        
result = zeros(m,n);

for i=1:m
	for j=1:n
           if im(i,j,1) > 95 && im(i,j,2) >40 && im(i,j,3)>20 ...
              && max([im(i,j,1),im(i,j,2),im(i,j,3)]) - min([im(i,j,1),im(i,j,2),im(i,j,3)])>15 ...
              && abs((im(i,j,1)-im(i,j,2)))>15 ...
              && im(i,j,1) > im(i,j,2) ...
              && im(i,j,1) > im(i,j,3)
			result(i,j)=1;      % ���
		end
	end
end

figure;
imshow(result);
title('��ֵ�����');

%��ֵͼ����̬ѧ����
Se1=ones(5);
Se2=ones(9);
result=imerode(result,Se1); 
figure;
imshow(result);
title('��ʴ���Ч��');
result=imdilate(result,Se2); 
figure;
imshow(result);
title('���ͺ��Ч��');

% ��ͨ�����ǣ�Ĭ��8��ͨ
% label���Ǳ����ͨ�����Ľ����numΪ��ͨ������
[label,num] = bwlabel(result,4);

box = regionprops(label,'BoundingBox');          % ��ȡ��ǿ�
centroid = regionprops(label,'Centroid');          % ��ȡ�������
proportion = regionprops(label,'Extent');          % ͬʱ�����������С�߽�����е����ر���

figure;
imshow(im), title('�������');
hold on
for i = 1:num
    % ��ʼx����ʼy��w��h
    bound = box(i).BoundingBox
    % �� ��
    h = bound(4);
    w = bound(3);
    area = h * w;
    % ������� 1/200�� ������ɫ������ռ���α���>0.6, ����/����
    if area > m * n / 200 && proportion(i).Extent > 0.6 && h/w > 0.5
        rectangle('position', box(i).BoundingBox, 'edgecolor','r','LineWidth', 2);                          % ����
        text(centroid(i,1).Centroid(1,1)-1,centroid(i,1).Centroid(1,2)-1, num2str(i),'Color', 'r')      % ���
    end
end
